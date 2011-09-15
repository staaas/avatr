class _CallCounter(object):
    __name__ = '_CallCounter'
    def __init__(self):
        self._cnt = 0

    def __call__(self, arg):
        self._cnt += 1
        return '%s_%s' % (self._cnt, arg)

def _get_random_provider_uid(alphabet='abcdefghijklmnopqrstuvwxyz1234567890',
                             length=10):
    import random
    rand_provider = ''.join(random.choice(alphabet) for _ in xrange(length))
    rand_uid = ''.join(random.choice(alphabet) for _ in xrange(length))
    return rand_provider, rand_uid
                 
def test_enable_cache_decorator():
    from cache import enable_cache

    rand_provider, rand_uid = _get_random_provider_uid()
    call_counter = enable_cache(rand_provider)(_CallCounter())

    res1 = call_counter(rand_uid)
    assert res1 == call_counter(rand_uid)
    assert res1 == call_counter(rand_uid)

    rand_provider, rand_uid = _get_random_provider_uid()
    call_counter = enable_cache(rand_provider)(_CallCounter())

    res2 = call_counter(rand_uid)
    assert res2 == call_counter(rand_uid)
    assert res1 != res2
