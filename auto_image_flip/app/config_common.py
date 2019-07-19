from pathlib import PurePath, Path
import os

TIMEZONE = 'Europe/Paris'


if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# Secret key for generating tokens
SECRET_KEY = os.environ.get("SECRET_KEY")

# Admin credentials
ADMIN_CREDENTIALS = os.environ.get("ADMIN_CREDENTIALS")

# Database choice
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
MAIL_SERVER = os.environ.get("MAIL_SERVER")
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