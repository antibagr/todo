from flask_login import UserMixin
from sqlalchemy import Column
from werkzeug.security import check_password_hash, generate_password_hash

from app.app.constants import ADMIN, INACTIVE, SEX_TYPES, STRING_LEN, USER, USER_ROLE, USER_STATUS
from app.app.extensions import db
from app.app.utils import get_current_time


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    phone = Column(db.String(STRING_LEN), nullable=False, default="")
    url = Column(db.String(STRING_LEN), nullable=False, default="")
    deposit = Column(db.Numeric, nullable=False, default=0.0)
    location = Column(db.String(STRING_LEN), nullable=False, default="")
    bio = Column(db.Text, default="")
    activation_key = Column(db.String(STRING_LEN))
    create_at = Column(db.DateTime, nullable=False, default=get_current_time)
    update_at = Column(db.DateTime)

    avatar = Column(db.String(STRING_LEN))

    _password = Column("password", db.String(200), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym("_password", descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    _sex = Column("sex", db.Integer, nullable=False, default=1)

    def _get_sex(self):
        return SEX_TYPES.get(self.sex)

    def _set_sex(self, sex):
        self._sex = sex

    sex = db.synonym("_sex", descriptor=property(_get_sex, _set_sex))

    # ================================================================
    role_code = Column(db.SmallInteger, default=USER, nullable=False)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    # ================================================================
    # One-to-many relationship between users and user_statuses.
    status_code = Column(db.SmallInteger, nullable=False, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = "%" + keyword + "%"
            criteria.append(
                db.or_(
                    User.name.ilike(keyword),
                    User.email.ilike(keyword),
                )
            )
        return cls.query.filter(map(db.and_, criteria))

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_name(self, name):
        return User.query.filter(db.and_(User.name == name, User.email != self.id)).count() == 0
