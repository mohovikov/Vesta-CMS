import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
BASE_DIR = Path(__file__).resolve().parent.parent

def load_version() -> str:
    try:
        with open("version") as f:
            return f.read().strip()
    except:
        return "Unknown"

class Config:
    APP_NAME = os.environ.get("APP_NAME", "Unknown")
    APP_VERSION = load_version()
    DEBUG = os.environ.get("DEBUG", False) in (True, "True")
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    TEMPLATES_FOLDER = os.path.join(BASE_DIR, "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
        username = os.environ.get("MYSQL_USERNAME", "root"),
        password = os.environ.get("MYSQL_PASSWORD", ""),
        host = os.environ.get("MYSQL_HOST", "localhost"),
        port = int(os.environ.get("MYSQL_PORT", "3306")),
        database = os.environ.get("MYSQL_DATABASE", "")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False