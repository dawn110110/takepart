import tornado.wsgi
import sae
from server import url_map, settings

#class MainHandler(tornado.web.RequestHandler):
#    Ref get(self):
#        self.write("Hello, world! - Tornado")
#
#url_map = [
#    (r'/$', MainHandler),
#]

app = tornado.wsgi.WSGIApplication(url_map, **settings)

application = sae.create_wsgi_app(app)
