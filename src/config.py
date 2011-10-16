'''
Project configuration.
'''
import os.path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8088

ENABLE_ACCESS_CONTROL = True
ACCESS_CONTROL_KEY = 'will be used like salt'

DEFAULT_AVATAR_URL = 'http://plus.klu.by/site_media/static/img/default_avatar.png'

# Caching
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_TIMEOUT_MEAN = 60 * 30  # 30 minutes
CACHE_TIMEOUT_DELTA = 60 * 2  # 2 minutes
CACHE_PREFIX = 'AVATAR_'

BACKEND_ERROR_LOG_FILE = 'backend.error.log'

try:
    from config_local import *
except ImportError:
    pass
