from flask import flash, redirect, render_template, url_for

from app import services, forms
from app.blueprints.admin import admin


@admin.get("/users")
def users():
    data = services.get_all_users()
    return render_template(
        "admin/users/list.html",
        _users = data.items,
        pagination = data
    )

@admin.route("/users/<int:id>/edit", methods = ["GET", "POST"])
def edit_user(id: int):
    user = services.get_user_by_id(id)
    form = forms.UserEditForm(obj = user)

    if not user:
        flash("Такого пользователя не существует", "warning")
        return redirect(url_for("admin.users", page = 1))

    if form.validate_on_submit():
        success, error = services.update_user_from_form(user, form)

        if success:
            flash("Изменения сохранены", "success")
            return redirect(url_for("admin.edit_user", id = user.id))

        flash(error if error else "Ошибка при сохранении данных. Пожалуйста, повторите попытку позже", "danger")

    return render_template(
        "admin/users/edit.html",
        user = user,
        form = form
    )