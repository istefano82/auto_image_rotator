import logging

from app.config_common import *


# DEBUG can only be set to True in a development environment for security reasons
DEBUG = True

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2
