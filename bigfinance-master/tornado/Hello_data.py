# -*- coding:UTF-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
#from tornado_similary import linear_B
from Http_Get_Data import get_db_and_close_2

from tornado.options import define,options

define("port",default=8000,help="run on the given port",type=int)

class BaseHandler(tornado.web.RequestHandler):
    # 这是自己定义的基类,业务类继承这个基类
    def __init__(self, *argc, **kwarg):
        super(BaseHandler, self).__init__(*argc, **kwarg)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.send_error(404)

    def mywrite(self, chunk):

        # 定义自己实现的write()方法
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if not isinstance(chunk, (list, dict)):
            message = "write() only accepts bytes, unicode, list and dict objects"
            raise TypeError(message)
        if isinstance(chunk, (list, dict)):
            chunk = json.dumps(chunk).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        #chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('public/404.html')
        elif status_code == 500:
            self.render('public/500.html')
        else:
            self.write('error' + str(status_code))

class IndexHandler(BaseHandler):
    '''
    def get(self):
        greeting = self.get_argument('greeting','Hello')
        self.mywrite(greeting + ',friendly user!')
    '''
    def get(self):

        code = self.get_argument('code')
        start = self.get_argument('start')
        #mid = self.get_argument('mid') # linear_C的新参数
        end = self.get_argument('end')

        #db = linear_B(code,start,end)
        dict_of_db = get_db_and_close_2(code, start, end)

        #self.mywrite(db)
        self.mywrite(dict_of_db)

if __name__== "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/",IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()