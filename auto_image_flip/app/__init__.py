from flask import Flask
import tensorflow as tf

from keras.layers import Dense,GlobalAveragePooling2D, Dropout
from keras.applications import MobileNet
from keras.models import Model
from keras.regularizers import l2
import tensorflow

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup Image deep learning model to run locally within the flask app.
# @app.before_first_request
# def load_model_to_app():
#     num_classes = 4
#
#     base_model = MobileNet(weights='imagenet',
#                            include_top=False)  # imports the mobilenet model and discards the last 1000 neuron layer.
#
#     x = base_model.output
#     x = GlobalAveragePooling2D()(x)
#     x = Dense(1024, activation='relu', kernel_regularizer=l2(0.01),
#               bias_regularizer=l2(0.01))(
#         x)  # we add dense layers so that the model can learn more complex functions and classify for better results.
#     x = Dropout(0.25)(x)
#     x = Dense(1024, activation='relu', kernel_regularizer=l2(0.01),
#               bias_regularizer=l2(0.01))(x)  # dense layer 2
#     x = Dropout(0.25)(x)
#     x = Dense(512, activation='relu', kernel_regularizer=l2(0.01),
#               bias_regularizer=l2(0.01))(x)  # dense layer 3
#     x = Dropout(0.5)(x)
#     preds = Dense(num_classes, activation='softmax')(x)  # final layer with softmax activation
#     app.model = Model(inputs=base_model.input, outputs=preds)
#     for layer in app.model.layers[:20]:
#         layer.trainable = False
#     for layer in app.model.layers[20:]:
#         layer.trainable = True
#     app.model.load_weights(app.config['MODEL_WEIGHTS'])
#     optimizer = tensorflow.train.AdamOptimizer(1e-5)
#     app.model.compile(optimizer=optimizer, loss='categorical_crossentropy',
#                   metrics=['accuracy'])
#     app.model.summary()
#     # Save the graph to the app framework.
#     app.graph = tf.get_default_graph()

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


