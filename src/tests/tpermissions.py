from hashlib import sha1
from datetime import datetime, timedelta

def test_validate_key():
    from permissions import _validate_key
    import config
    
    key1 = sha1(config.ACCESS_CONTROL_KEY + \
                datetime.utcnow().strftime('%Y%m%d%H')).hexdigest()
    assert _validate_key(key1)

    hour_ago = datetime.utcnow() - timedelta(hours=1)
    key2 = sha1(config.ACCESS_CONTROL_KEY + \
                hour_ago.strftime('%Y%m%d%H')).hexdigest()
    assert _validate_key(key2)

    hours_ago = datetime.utcnow() - timedelta(hours=2)
    key3 = sha1(config.ACCESS_CONTROL_KEY + \
                hours_ago.strftime('%Y%m%d%H')).hexdigest()
    assert not _validate_key(key3)

    hour_forward = datetime.utcnow() + timedelta(hours=1)
    key4 = sha1(config.ACCESS_CONTROL_KEY + \
                hours_ago.strftime('%Y%m%d%H')).hexdigest()
    assert not _validate_key(key4)

    key5 = sha1(config.ACCESS_CONTROL_KEY + 'something' + \
                datetime.utcnow().strftime('%Y%m%d%H')).hexdigest()
    assert not _validate_key(key5)
