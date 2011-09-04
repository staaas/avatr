"""
Avatarizaor web.py application powered by gevent
"""

from gevent import monkey; monkey.patch_all()

from gevent.pywsgi import WSGIServer
import web

import backends
import config
from permissions import enable_access_control

urls = ('/(\w+)/(\d+)', 'avatar')

provider_mapping = {'twitter':  backends.twitter,
                    'vkontakte': backends.vkontakte,
                    'facebook': backends.facebook,}

class avatar:
    # Since gevent's WSGIServer executes each incoming connection in a separate greenlet
    # long running requests such as this one don't block one another;
    # and thanks to "monkey.patch_all()" statement at the top, thread-local storage used by web.ctx
    # becomes greenlet-local storage thus making requests isolated as they should be.
    @enable_access_control
    def GET(self, provider, uid):
        avatar_url = provider_mapping.get(provider, lambda uid: None)(uid)
        return web.tempredirect(avatar_url or config.DEFAULT_AVATAR_URL)


if __name__ == "__main__":
    application = web.application(urls, globals()).wsgifunc()
    WSGIServer(('', 8088), application).serve_forever()