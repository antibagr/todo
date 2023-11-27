from wtforms import (
    BooleanField,
    EmailField,
    Form,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.app.constants import (
    AGREE_TIP,
    EMAIL_LEN_MAX,
    EMAIL_LEN_MIN,
    EMAIL_TIP,
    PASSWORD_LEN_MAX,
    PASSWORD_LEN_MIN,
    PASSWORD_TIP,
    USERNAME_LEN_MAX,
    USERNAME_LEN_MIN,
    USERNAME_TIP,
)
from app.app.user import User


class LoginForm(Form):
    next = HiddenField()
    login = StringField(
        "Username or email", [DataRequired(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)]
    )
    password = PasswordField(
        "Password", [DataRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)]
    )
    remember = BooleanField("Remember me")
    # Use render_kw to set style of submit button
    submit = SubmitField("Sign in", render_kw={"class": "btn btn-success btn-block"})


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(
        "Email",
        [DataRequired(), Email(), Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)],
        description=EMAIL_TIP,
    )
    password = PasswordField(
        "Password",
        [DataRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
        description=PASSWORD_TIP,
    )
    name = StringField(
        "Choose your username",
        [DataRequired(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
        description=USERNAME_TIP,
    )
    agree = BooleanField(AGREE_TIP, [DataRequired()])
    submit = SubmitField("Sign up", render_kw={"class": "btn btn-success btn-block"})

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError("This username is taken")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is taken")


class RecoverPasswordForm(Form):
    email = EmailField(
        "Your email", [DataRequired(), Email(), Length(EMAIL_LEN_MIN, EMAIL_LEN_MAX)]
    )
    submit = SubmitField("Send instructions")


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField("Password", [DataRequired()])
    password_again = PasswordField(
        "Password again", [EqualTo("password", message="Passwords don't match")]
    )
    submit = SubmitField("Save")


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(
        "Password", [DataRequired(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)]
    )
    submit = SubmitField("Reauthenticate")
