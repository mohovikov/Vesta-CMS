import os
from flask import render_template

from app.blueprints.site import site
from app.config import BASE_DIR


@site.get("/")
def index():
    return render_template("site/index.html")

@site.get('/license')
def license():
    with open(os.path.join(BASE_DIR, 'LICENSE'), 'r', encoding='utf-8') as f:
        license_text = f.read()
    return render_template('site/license.html', license_text=license_text)