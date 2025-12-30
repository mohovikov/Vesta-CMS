from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )
    username: Mapped[str] = mapped_column(
        String(30),
        nullable = False,
        unique = True
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable = False,
        unique = True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )
    privileges: Mapped[int] = mapped_column(
        BigInteger,
        nullable = False
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        nullable = False
    )

    def set_password(self, password: str) -> None:
        """Хэширует пароль и сохраняет"""
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password: str) -> bool:
        """Проверяет пароль по хэшу"""
        return check_password_hash(self.password, password)

    def __init__(self, username: str, email: str, privileges: int) -> None:
        self.username = username
        self.email = email
        self.privileges = privileges

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
    