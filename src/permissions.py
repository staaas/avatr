'''
Access control tools
'''
from hashlib import sha1
from datetime import datetime, timedelta
from functools import wraps

import config

_KEY_TIMESTAMP_FORMAT = '%Y%m%d%H'

def validate_key(key):
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
