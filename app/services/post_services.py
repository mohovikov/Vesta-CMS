from sqlalchemy.exc import IntegrityError

from app import forms
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