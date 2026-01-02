from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app import services, forms
from app.blueprints.admin import admin


@admin.get("/posts")
def posts():
    data = services.get_all_posts()
    return render_template(
        "admin/posts/list.html",
        _posts = data.items,
        pagination = data
    )

@admin.route("/posts/add", methods=["GET", "POST"])
def add_post():
    form = forms.PostForm()

    if form.validate_on_submit():
        success, message = services.add_post(form, current_user.id)

        if success:
            flash(message, "success")
            return redirect(url_for("admin.posts", page = 1))

        flash(message, "error")

    return render_template(
        "admin/posts/add.html",
        form = form
    )

@admin.route("/posts/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id: int):
    post = services.get_post_by_id(id)

    if not post:
        flash("Такой новости не существует", "warning")
        return redirect(url_for("admin.posts", page = 1))

    form = forms.PostForm(obj=post)

    if form.validate_on_submit():
        success, error = services.save_edit_post(post, form)

        if success:
            flash("Статья успешно обновлена и сохранена.", "success")
            return redirect(url_for("admin.edit_post", id = post.id))

        flash(error if error else "Ошибка при сохранении данных. Пожалуйста, повторите попытку позже", "danger")

    return render_template(
        "admin/posts/edit.html",
        post = post,
        form = form
    )