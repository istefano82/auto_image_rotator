from pathlib import PurePath, Path
import os

TIMEZONE = 'Europe/Paris'

# Secret key for generating tokens
SECRET_KEY = os.environ.get("SECRET_KEY", "houdini")

# Admin credentials
ADMIN_CREDENTIALS = (os.environ.get("ADMIN_USER"), os.environ.get(
    "ADMIN_PASSWORD"))

# Database choice
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
ADMINS = [os.environ.get("ADMINS")]

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

UPLOAD_FOLDER = PurePath(Path(__file__).resolve().parent, 'static/uploads')
MODEL_WEIGHTS = PurePath(Path(__file__).resolve().parent, 'static/saved_model/image_rotate_weights.h5')
HEROKU_MODEL_APP_URL = 'https://image-rotation-detector.herokuapp.com'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'JPEG'])