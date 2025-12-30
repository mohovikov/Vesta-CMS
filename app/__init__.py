from flask import Flask

from app.config import Config
from app.constants import Privileges
from app.extensions import login_manager, db, migrate


def create_app() -> Flask:
    app = Flask(
        import_name = __name__,
        template_folder = Config.TEMPLATES_FOLDER,
        static_folder = Config.STATIC_FOLDER
    )
    app.config.from_object(Config)

    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    from app.blueprints.api import api
    app.register_blueprint(api)

    from app.blueprints.admin import admin
    app.register_blueprint(admin)

    from app.blueprints.site import site
    app.register_blueprint(site)


    @app.context_processor
    def inject_app_info():
        return dict(
            app_name = app.config.get("APP_NAME"),
            app_version = app.config.get("APP_VERSION"),
            privileges = Privileges,
            privileges_list = Privileges.get_privileges_list
        )

    return app