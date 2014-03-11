#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
from utils import re_compile
import os
import json
import tornado.web
import tornado.wsgi
import tornado.httpserver
import logging
import traceback

class BaseHandler(tornado.web.RequestHandler):
    pass


class BaiduVcode(object):
    """ 验证码， 使用 Baidu 地图 的开放接口 """
    def verify(self, vcode, code):
        try:
            import urllib2
            res = urllib2.urlopen("http://map.baidu.com/maps/services/captcha/verify?code=%s&vcode=%s" % (code, vcode)).read()
            res_ob = json.loads(res)
            if int(res_ob['result']['error']) == 0:
                return True, res
            else:
                logging.warning("vcode fail, result_ob = %r" % res_ob)
                return False, res
        except Exception as e:
            logging.error(traceback.format_exc())
            return False, '{ "result": { "error": -1, "error_message": "server_internal_error" } } '


class VcodeTest(BaseHandler, BaiduVcode):
    def post(self):
        vcode = self.get_argument("vcode")
        code = self.get_argument("code")
        cb_func = self.get_argument("callback")
        ok, res = self.verify(vcode, code)
        print ok, res
        if ok:
            self.write("%s(%s)" % (cb_func, res))
        else:
            self.write("%s(%s)" % (cb_func, res))
            self.write(res)


    def get(self):
        self.post()

class IndexHandler(BaseHandler):
    '''home page'''
    def get(self):
        self.render("index.html")

class ContestList(BaseHandler):
    """ 假的比赛列表"""
    def post(self):
        cb_func = self.get_argument("callback")
        contest_list = [
                {"cid": 1, "name": u"小游戏开发大赛", "description" : u"宝宝博阿波啊<h1>asdasd</h1>", "endtime": 1394552244},
                {"cid": 2, "name": u"Linux挑战赛", "description" : u"宝宝博阿波啊<h1>asdasd</h1>", "endtime": 1394512242},
                {"cid": 3, "name": u"网星杯", "description" : u"宝宝博阿波啊<h1>asdasd</h1>", "endtime": 1394512242},
                {"cid": 4, "name": u"Imagine Cup", "description" : u"宝宝博阿波啊<h1>asdasd</h1>", "endtime": 1394552244},
                {"cid": 5, "name": u"数模", "description" : u"宝宝博阿波啊<h1>asdasd</h1>", "endtime": 1394552244},
                ]
        self.write("%s(%s)" % (cb_func, json.dumps(contest_list, encoding="utf-8", ensure_ascii=False)))
    def get(self):
        self.post()

class TakePart(BaseHandler):
    def post(self):
        pass



settings = {
    "debug": True,
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "cookie_secret": "61eJJaaah7EQnp2XdTP1o/VooETzKXQAGaYdkL5gEmG=",
}

url_map = [
    (r'/$', IndexHandler),
    (r'/contest_list$', ContestList),
    (r'/vcode_test$', VcodeTest),
    (r'/static/(.*)',
        tornado.web.StaticFileHandler,
        dict(path=settings['static_path'])),
]


application = tornado.web.Application(url_map, **settings)

def main():
    vc = BaiduVcode()
    vc.verify("303531303134353130353234353031366D61705F76636F64655F7365637265743133393435353335353730343031303130313069DE2E670DE3D04AFA73ABF7C4BC94", "N57H")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)

    tornado.options.parse_command_line(sys.argv)

    if settings['debug']:  # if debug on, change logging level
        logging.getLogger().setLevel(logging.DEBUG)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
