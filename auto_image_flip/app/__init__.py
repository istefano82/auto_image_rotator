from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Use .env to setup enviroment variables
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup the logger
from app.logger_setup import logger

# Setup the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask.ext.mail import Mail
mail = Mail(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

# Setup the password crypting
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app.views import main, user, error
app.register_blueprint(user.userbp)

# Setup the user login process
from flask.ext.login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()

from app import admin



