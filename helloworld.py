import tornado.ioloop
import tornado.web
import tornado.escape
import tornado
import json
import tornadoredis
# handler / django wiews analog
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

c = tornadoredis.Client()
# c.connect()
ttl = 5
class GenAsyncHandler(tornado.web.RequestHandler):
    async def get(self):
        if await tornado.gen.Task(c.exists, 'rates'):
            res = await tornado.gen.Task(c.get, 'rates')
        else:
            http_client = AsyncHTTPClient()
            response = await http_client.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
            res_dict = json.loads(response.body.decode())
            res = res_dict['bpi']['USD']['rate']
        await tornado.gen.Task(c.set,'rates', res, ttl)
        self.write('Bitcoin curs is %s$' %res)


def make_app():
    # constructor
    return tornado.web.Application([
        (r"/", GenAsyncHandler),
        (r"/new_order", GenAsyncHandler),
        (r"/status/(?P<pk>\d+)", GenAsyncHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


# class GenAsyncHandler(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     @tornado.gen.engine
#     async def get(self):
#         foo =
#         return tornado.gen.Task(c.get, 'foo')
#         self.set_header('Content-Type', 'text/html')
#         self.render("template.html", title="Simple demo", foo=foo)
#
#         http_client = AsyncHTTPClient()
#         response = await http_client.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
#         res = json.loads(response.body.decode())
#         self.write('Bitcoin curs is %s$' % res['bpi']['USD']['rate'])
#         # self.render("template.html")