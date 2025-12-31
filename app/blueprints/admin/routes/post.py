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