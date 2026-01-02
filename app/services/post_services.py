from sqlalchemy.exc import IntegrityError

from app import forms
from app.helpers import post as post_helper
from app.extensions import db
from app.models import Post


def get_all_posts(page: int = 1, per_page: int = 25):
    return Post.query.order_by(Post.id.asc()).paginate(page = page, per_page = per_page, error_out = False)

def get_post_by_id(id: int) -> Post | None:
    return Post.query.get(id)

def add_post(form: forms.PostForm, author_id: int) -> tuple[bool, str]:
    """
    Создаёт новый пост на основе формы.
    Возвращает (успех, сообщение об ошибке).
    """
    if not form.validate_on_submit():
        return False, "Некорректные данные формы"

    post = Post(
        title = str(form.title.data).strip(),
        slug = str(form.slug.data).strip() if form.slug.data else Post.generate_slug(str(form.title.data)),
        excerpt = str(form.excerpt.data).strip(),
        content = str(form.content.data).strip(),
        status = form.status.data
    )
    post.author_id = author_id

    try:
        db.session.add(post)
        db.session.commit()
        return True, "Пост успешно создан"
    except IntegrityError:
        db.session.rollback()
        return False, "Пост с таким slug уже существует"
    except Exception as e:
        db.session.rollback()
        return False, f"Ошибка при создании поста: {e}"

def save_edit_post(post: Post, form: forms.PostForm) -> tuple[bool, str | None]:
    title = str(form.title.data).strip()
    excerpt = str(form.excerpt.data).strip()
    content = str(form.content.data).strip()

    post.title = title
    post.slug = str(form.slug.data).strip() if form.slug.data else Post.generate_slug(title)
    post.excerpt = excerpt
    post.content = content
    post.status = form.status.data

    post.meta_title = form.meta_title.data or post_helper.generate_meta_title(title)
    post.meta_description = form.meta_description.data or post_helper.generate_meta_description(excerpt or content)

    if form.meta_keywords.data:
        post.meta_keywords = post_helper.clean_meta_keywords(form.meta_keywords.data)
    else:
        post.meta_keywords = post_helper.generate_meta_keywords(excerpt or content)

    try:
        db.session.commit()
        return True, None

    except IntegrityError:
        db.session.rollback()
        return False, "Статья не сохранена. Статья с таким названием или URL уже существует."

    except Exception:
        db.session.rollback()
        return False, "Статья не сохранена. Произошла ошибка. Пожалуйста, повторите попытку позже."