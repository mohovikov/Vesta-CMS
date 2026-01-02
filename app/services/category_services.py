from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import forms
from app.extensions import db
from app.constants import PostStatus
from app.models import Category, Post


def get_all_categories(page: int = 1, per_page: int = 25):
    return Category.query.order_by(Category.id.asc()).paginate(page = page, per_page = per_page, error_out = False)

def get_category_by_id(id: int) -> Category | None:
    return Category.query.get(id)

def get_posts_count_for_categories(categories: list[Category], only_published: bool = True) -> dict[int, int]:
    """
    Возвращает словарь {category_id: posts_count} для списка категорий
    """
    query = db.session.query(
        Post.category_id,
        func.count(Post.id).label("posts_count")
    )

    if only_published:
        query = query.filter(Post.status == PostStatus.PUBLISHED)

    query = query.filter(Post.category_id.in_([c.id for c in categories]))
    query = query.group_by(Post.category_id)

    return {row.category_id: row.posts_count for row in query.all()}

def add_category(form: forms.CategoryForm) -> tuple[bool, str]:
    title = str(form.title.data).strip()
    slug = str(form.slug.data).strip()
    description = str(form.description.data).strip() or None
    is_active = bool(form.is_active.data)

    category = Category(
        title = title,
        slug = slug if slug else Category.generate_slug(title),
        description = description,
        is_active = is_active
    )

    try:
        db.session.add(category)
        db.session.commit()
        return True, "Категория успешно создана"
    except IntegrityError:
        db.session.rollback()
        return False, "Категория с таким slug уже существует"
    except Exception as e:
        db.session.rollback()
        return False, f"Ошибка при создании категории: {e}"

def save_edit_category(category: Category, form: forms.CategoryForm) -> tuple[bool, str]:
    title = str(form.title.data).strip()
    slug = str(form.slug.data).strip() or Category.generate_slug(title)
    description = str(form.description.data).strip()
    is_active = bool(form.is_active.data)

    category.title = title
    category.slug = slug
    category.description = description
    category.is_active = is_active

    try:
        db.session.commit()
        return True, "Категория успешно обновлена и сохранена."

    except IntegrityError:
        db.session.rollback()
        return False, "Категория не сохранена. Статья с таким названием или URL уже существует."

    except Exception:
        db.session.rollback()
        return False, "Категория не сохранена. Произошла ошибка. Пожалуйста, повторите попытку позже."