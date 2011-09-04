'''
Logging for backends.
'''
import logging
from functools import wraps
import urllib2

import config


logger = logging.getLogger('backends')
hdlr = logging.FileHandler(config.BACKEND_ERROR_LOG_FILE)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)


def enable_logging(func):
    '''
    Decorator enabling logging for backends.
    It catches and logs well known exceptions, such as URLError, ValueError
    or TypeError, and logs (without catching) all other exceptions.
    '''
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (urllib2.URLError, TypeError, ValueError):
            logger.exception('Caught exception in backend %s' % func.__name__)
        except Exception:
            logger.exception('Uncaught exception in backend %s' % func.__name__)
            raise
        return None
    return decorated_func
