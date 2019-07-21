import logging

from app.config_common import *


# DEBUG has to be to False in a production environment for security reasons
DEBUG = False

LOG_LEVEL = logging.INFO
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2