from typing import Optional
from sqlalchemy.exc import IntegrityError

from app import forms
from app.models import User
from app.extensions import db


def get_all_users(page: int = 1, per_page: int = 25):
    return User.query.order_by(User.id.asc()).paginate(page = page, per_page = per_page, error_out = False)

def get_user_by_id(id: int) -> User | None:
    return User.query.get(id)

def get_users_count() -> int:
    return User.query.count()

def register_user(form: forms.RegisterForm) -> tuple[bool, str]:
    """
    Регистрирует пользователя на основе формы.
    Возвращает (success, error_message)
    """

    if (
        form.email.data is None
        or form.username.data is None
        or form.password.data is None
    ):
        return False, "Некорректные данные формы"

    user = User(
        username = form.username.data.strip(),
        email = form.email.data.lower().strip(),
        privileges = 1
    )

    user.set_password(form.password.data)

    db.session.add(user)

    try:
        db.session.commit()
        return True, ""
    except IntegrityError:
        db.session.rollback()
        return False, "Пользователь с таким email или именем уже существует"

def authenticate_user(form: forms.LoginForm) -> tuple[Optional[User], str]:
    """
    Проверяет данные авторизации.
    """

    if (
        form.email.data is None
        or form.password.data is None
    ):
        return None, "Некорректные данные формы"

    user = User.query.filter_by(
        email = form.email.data.lower().strip()
    ).first()

    if not user or not user.check_password(form.password.data):
        return None, "Неверный email или пароль"

    return user, ""

def update_user_from_form(user: User, form: forms.UserEditForm) -> tuple[bool, str | None]:
    """
    Обновляет данные пользователя на основе формы редактирования.

    :param user: объект User (SQLAlchemy)
    :param form: UserEditForm
    :return: (success, error_message)
    """

    # Базовые поля
    user.username = str(form.username.data).strip()
    user.email = str(form.email.data).strip()
    user.privileges = int(str(form.privileges.data))

    # Пароль — только если введён
    if form.password.data:
        user.set_password(form.password.data)

    try:
        db.session.commit()
        return True, None

    except IntegrityError:
        db.session.rollback()
        return False, "Пользователь с таким именем или email уже существует"

    except Exception:
        db.session.rollback()
        return False, "Не удалось сохранить изменения. Пожалуйста, повторите попытку позже"
