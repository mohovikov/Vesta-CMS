from flask import flash, redirect, render_template, url_for

from app import services, forms
from app.blueprints.admin import admin


@admin.get("/categories")
def categories():
    data = services.get_all_categories()
    counts = services.get_posts_count_for_categories(data.items)
    return render_template(
        "admin/categories/list.html",
        _categories = data.items,
        counts = counts
    )

@admin.route("/categories/add", methods=["GET", "POST"])
def add_category():
    form = forms.CategoryForm()

    if form.validate_on_submit():
        success, message = services.add_category(form)

        if success:
            flash(message, "success")
            return redirect(url_for("admin.categories", page = 1))

        flash(message, "error")

    return render_template(
        "admin/categories/add.html",
        form = form
    )

@admin.route("/categories/<int:id>/edit", methods=["GET", "POST"])
def edit_category(id: int):
    category = services.get_category_by_id(id)

    if not category:
        flash("Такой категории не существует", "warning")
        return redirect(url_for("admin.categories", page = 1))

    form = forms.CategoryForm(obj=category)

    if form.validate_on_submit():
        success, message = services.save_edit_category(category, form)

        if success:
            flash(message, "success")
            return redirect(url_for("admin.categories", page = 1))

        flash(message, "error")

    return render_template(
        "admin/categories/edit.html",
        category = category,
        form = form
    )