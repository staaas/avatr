'''
WSGI-helpers.
'''
import logging

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, Forbidden, InternalServerError

from permissions import validate_key


logger = logging.getLogger('app')
logger.setLevel(logging.ERROR)


class KeyProtectedApp(object):
    '''
    Base class for a WSGI-app with a GET paramter based auhtentication.
    '''
    @property
    def routing(self):
        '''
        Must return a dict like {'url':'endpoint'}
        '''
        raise NotImplementedError
    
    def __init__(self):
        self.url_map = Map(
            [Rule(k, endpoint=v) for k, v in self.routing.iteritems()])

    def dispatch_request(self, request):
        if not validate_key(request.args.get('key', '')):
            raise Forbidden
        endpoint, kw = self.url_map.bind_to_environ(request.environ).match()
        return getattr(self, endpoint)(request, **kw)

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            response = self.dispatch_request(request)
        except HTTPException, e:
            response = e
        return response(environ, start_response)

