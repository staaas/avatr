'''
Access control tools
'''
from hashlib import sha1
from datetime import datetime, timedelta
from functools import wraps

import web

import config

_KEY_TIMESTAMP_FORMAT = '%Y%m%d%H'

def _validate_key(key):
    '''
    Checking for the key which is valid for two hours.

    The key must be generated with
    sha1(config.ACCESS_CONTROL_KEY +\
    datetime.utcnow().strftime(_KEY_TIMESTAMP_FORMAT)).hexdigest()
    '''
    now = datetime.utcnow()
    key_candidate = sha1(config.ACCESS_CONTROL_KEY + \
                          now.strftime(_KEY_TIMESTAMP_FORMAT)).hexdigest()
    if key == key_candidate:
        return True

    hour_ago = now - timedelta(hours=1)
    key_candidate = sha1(config.ACCESS_CONTROL_KEY + \
                          hour_ago.strftime(_KEY_TIMESTAMP_FORMAT)).hexdigest()

    if key == key_candidate:
        return True

    return False


def enable_access_control(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        '''
        Checks whether the request with the given key should be processed.
        '''
        if config.ENABLE_ACCESS_CONTROL:
            if not _validate_key(web.input(key='').key):
                return web.forbidden()
        return func(*args, **kwargs)
    return decorated_func
