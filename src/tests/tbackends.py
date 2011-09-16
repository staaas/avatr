import re

def test_vkontakte():
    from backends import vkontakte

    uid = 21630707
    re_pattern = '^http://.*\.vkontakte\.ru/u%s/.*\.\w{3,4}$' % uid

    assert re.match(re_pattern, vkontakte(uid))

def test_twitter():
    from backends import twitter

    uid = '238548627'
    re_pattern = 'http://.*\.twimg\.com/profile_images/.*/.*_normal\.\w{3,4}'

    assert re.match(re_pattern, twitter(uid))

def test_facebook():
    from backends import facebook

    uid = 100001906253071
    pattern = 'http://graph.facebook.com/%s/picture' % uid

    assert pattern == facebook(uid)
