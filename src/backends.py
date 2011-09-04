'''
This module defines backends, which are provider-specific functions,
returning url to user avatar by uid.
'''
import urllib2
import json

import gevent
from gevent.coros import Semaphore

from cache import enable_cache
from log import enable_logging

@enable_cache('twitter')
@enable_logging
def twitter(uid):
    ' Twitter backend '
    twi_data = urllib2.urlopen('http://api.twitter.com/1/users/show.json?user_id=%s' % uid).read()
    avatar = json.loads(twi_data).get('profile_image_url', None)
    return avatar


# There must be not more than 3 requests to vkontakte per second,
# that is why we use Semaphore and gevent.sleep
vkontakte_semaphore = Semaphore(1)
    
@enable_cache('vkontakte')
@enable_logging
def vkontakte(uid):
    ' Vkontakte backend '
    vkontakte_semaphore.acquire()
    vk_data = urllib2.urlopen('https://api.vkontakte.ru/method/getProfiles?uids=%s&fields=photo' % uid).read()
    avatar = json.loads(vk_data).get('response', [{}])[0]['photo']
    gevent.sleep(0.34)  # we shouldn't make more than 3 requests per second!
    vkontakte_semaphore.release()
    return avatar

@enable_logging
def facebook(uid):
    ' Facebook backend '
    return 'http://graph.facebook.com/%s/picture' % uid