from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError
)

from app.models import User
from app.extensions import db


class RegisterForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(message="Введите имя пользователя"),
            Length(min=3, max=30)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введите email"),
            Email(message="Некорректный email"),
            Length(max=50)
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введите пароль"),
            Length(min=8, max=128)
        ]
    )

    confirm_password = PasswordField(
        "Подтверждение пароля",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли не совпадают")
        ]
    )

    def validate_username(self, field):
        if db.session.query(User.id).filter_by(username=field.data).first():
            raise ValidationError("Имя пользователя уже занято")

    def validate_email(self, field):
        email = field.data.lower().strip()
        if db.session.query(User.id).filter_by(email=email).first():
            raise ValidationError("Email уже используется")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введите email"),
            Email(message="Некорректный email"),
            Length(max=50)
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введите пароль")
        ]
    )