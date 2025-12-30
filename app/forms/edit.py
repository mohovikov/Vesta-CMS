from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional, NumberRange


class UserEditForm(FlaskForm):
    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(message="Имя пользователя обязательно"),
            Length(min=3, max=30),
        ],
        render_kw={
            "class": "form-control",
            "autocomplete": "off",
        },
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email обязателен"),
            Email(message="Некорректный email"),
            Length(max=50),
        ],
        render_kw={
            "class": "form-control",
        },
    )

    password = PasswordField(
        "Новый пароль",
        validators=[
            Optional(),
            Length(min=8, max=255),
        ],
        render_kw={
            "class": "form-control",
            "autocomplete": "new-password",
            "placeholder": "Оставьте пустым, чтобы не менять",
        },
    )

    privileges = IntegerField(
        "Привилегии",
        validators=[
            DataRequired(message="Укажите уровень привилегий"),
            NumberRange(min=0),
        ],
        render_kw={
            "class": "form-control",
        },
    )
