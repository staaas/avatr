"""
Avatarizaor web.py application powered by gevent
"""

from gevent import monkey; monkey.patch_all()

from gevent.pywsgi import WSGIServer
from werkzeug.utils import redirect

import backends
import config
import wsgi

provider_mapping = {'twitter':  backends.twitter,
                    'vkontakte': backends.vkontakte,
                    'facebook': backends.facebook,}

class Avatr(wsgi.KeyProtectedApp):
    routing = {'/<backend>/<int:uid>': 'avatar'}

    def avatar(self, request, backend, uid):
        avatar_url = provider_mapping.get(backend, lambda uid: None)(uid)
        return redirect(avatar_url or config.DEFAULT_AVATAR_URL)

if __name__ == "__main__":
    application = Avatr()
    WSGIServer((config.SERVER_HOST, config.SERVER_PORT),
               application).serve_forever()