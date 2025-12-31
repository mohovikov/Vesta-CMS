from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import PostStatus
from app.extensions import db

if TYPE_CHECKING:
    from app.models import User


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete = "CASCADE"),
        nullable = False
    )
    title: Mapped[str] = mapped_column(String(255), nullable = False)
    excerpt: Mapped[str] = mapped_column(Text, nullable = False)
    content: Mapped[str] = mapped_column(Text, nullable = False)

    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, name = "post_status_enum"),
        nullable = False,
        default = PostStatus.MODERATION,
        server_default = PostStatus.MODERATION.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("UTC_TIMESTAMP()"),
        nullable = False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = text("UTC_TIMESTAMP()"),
        server_onupdate = text("UTC_TIMESTAMP()"),
        nullable = False
    )

    author: Mapped["User"] = relationship(
        back_populates = "posts"
    )