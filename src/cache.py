'''
Avatar caching tools.
'''
import random
from functools import wraps

import redis

import config

_redis_client = redis.Redis(host=config.CACHE_REDIS_HOST,
                            port=config.CACHE_REDIS_PORT,
                            db=config.CACHE_REDIS_DB)

def _get_key(provider, uid):
    ' Returns memcache key for the given provider and url '
    return '%s%s_%s' % (config.CACHE_PREFIX, provider, uid)

def _get_timeout():
    '''
    Returns randomized timeout.
    If we have several cache items added during a short period of time, these
    items will be expired not at the same time.'
    '''
    return random.randint(config.CACHE_TIMEOUT_MEAN - config.CACHE_TIMEOUT_DELTA,
                          config.CACHE_TIMEOUT_MEAN + config.CACHE_TIMEOUT_DELTA)
    
def _get_avatar(provider, uid):
    ' Getting avatar url from cache '
    key = _get_key(provider, uid)
    return _redis_client.get(key)

def _set_avatar(provider, uid, avatar):
    ' Setting avatar in cache '
    if avatar:
        key = _get_key(provider, uid)
        _redis_client.set(key, avatar)
        _redis_client.expire(key, _get_timeout())
    return avatar

def enable_cache(provider):
    '''
    Decorator for some backend that tries to take the value from cache
    before calling the backend.
    If this value doen't exist in cache, we call the backend and put its
    result into cache.
    '''
    def enable_cache_decorator(func):
        @wraps(func)
        def decorated_func(uid):
            avatar = _get_avatar(provider, uid)
            if avatar:
                return avatar
            return _set_avatar(provider, uid, func(uid))
        return decorated_func
    return enable_cache_decorator
