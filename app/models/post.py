from datetime import datetime
from markupsafe import Markup, escape
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from slugify import slugify

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
    slug: Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
    excerpt: Mapped[str] = mapped_column(Text, nullable = False)
    content: Mapped[str] = mapped_column(Text, nullable = False)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus, name = "post_status_enum"),
        nullable = False,
        default = PostStatus.DRAFT,
        server_default = PostStatus.DRAFT.value
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

    def __init__(
            self,
            title: str,
            slug: str,
            excerpt: str,
            content: str,
            status: PostStatus = PostStatus.DRAFT
            ) -> None:
        self.title = title
        self.slug = slug
        self.excerpt = excerpt
        self.content = content
        self.status = status

    @staticmethod
    def generate_slug(title: str) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while Post.query.filter_by(slug = slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def status_badge(self) -> Markup:
        config = {
            PostStatus.DRAFT: {
                "label": "Черновик",
                "color": "secondary",
                "icon": "fa-pen",
            },
            PostStatus.MODERATION: {
                "label": "На модерации",
                "color": "info",
                "icon": "fa-hourglass-half",
            },
            PostStatus.PUBLISHED: {
                "label": "Опубликован",
                "color": "success",
                "icon": "fa-check",
            },
            PostStatus.ARCHIVED: {
                "label": "В архиве",
                "color": "warning",
                "icon": "fa-box-archive",
            },
            PostStatus.DELETED: {
                "label": "Удалён",
                "color": "danger",
                "icon": "fa-trash",
            },
        }

        data = config.get(self.status)

        if not data:
            return Markup(
                '<span class="badge bg-secondary">Неизвестно</span>'
            )

        return Markup(f'''
            <span class="badge bg-{data["color"]}">
                <i class="fa-solid {data["icon"]} me-1"></i>
                <span>{data["label"]}</span>
            </span>
        ''')
    
    def short_title(self, limit: int = 30) -> Markup:
        title = self.title or ""

        if len(title) <= limit:
            return escape(title)

        short = title[:limit].rstrip() + "…"

        return Markup(
            f'''
            <span
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="{escape(title)}"
            >
                {escape(short)}
            </span>
            '''
        )