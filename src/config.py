import os
from dotenv import load_dotenv


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

FLASK_HOST = os.getenv("FLASK_HOST")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5001))

SECRET_KEY = os.urandom(32)

POSTGRES_DB = os.getenv("DATABASE_DATABASE")
POSTGRES_HOST = os.getenv("DATABASE_HOST")
POSTGRES_USER = os.getenv("DATABASE_USERNAME")
POSTGRES_PASS = os.getenv("DATABASE_PASSWORD")
POSTGRES_PORT = int(os.getenv("DATABASE_PORT", 5432))
POSTGRES_SCHEMA = os.getenv("DATABASE_NAME")

POLIGONS_GEOJSON_PATH = "src/polygons.geojson"
RAW_DATA_PATH = "raw"

DEBUG = True
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?options=--search_path={POSTGRES_SCHEMA}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
