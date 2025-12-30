from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app import forms, services
from app.blueprints.site import site


@site.route("/register", methods = ['GET', 'POST'])
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        success, message = services.register_user(form)

        if success:
            flash("Аккаунт успешно создан, теперь вы можете войти!", "success")
            return redirect(url_for("site.login"))
        else:
            flash(message, "danger")
            return render_template("site/register.html", form=form)

    return render_template(
        "site/register.html",
        form = form
    )

@site.route("/login", methods = ['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user, message = services.authenticate_user(form)

        if not user:
            flash(message, "danger")
            return render_template("site/login.html", form=form)

        # Если используешь Flask-Login
        login_user(user)

        flash(f"С возвращением, {user.username}", "success")
        return redirect(url_for("site.index"))

    return render_template(
        "site/login.html",
        form = form
    )

@login_required
@site.get("/logout")
def logout():
    logout_user()
    return redirect(url_for('site.index'))