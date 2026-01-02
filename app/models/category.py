from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


if TYPE_CHECKING:
    from app.models import Post

class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False,
        unique = True
    )
    slug: Mapped[str] = mapped_column(
        String(255),
        nullable = False,
        unique = True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable = True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default = True,
        index = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        server_default = text("UTC_TIMESTAMP()"),
        nullable = False
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates = "category"
    )

    def __init__(
        self,
        title: str,
        slug: str,
        description: str | None,
        is_active: bool = True
    ) -> None:
        self.title = title
        self.slug = slug
        self.description = description
        self.is_active = is_active