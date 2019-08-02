
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import numpy as np 
import get_http_data
#from tornado_similary import linear_B
#from linear_A import linear_C

from tornado.options import define,options

define("port",default=8000,help="run on the given port",type=int)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    # 这是自己定义的基类,业务类继承这个基类
    def __init__(self, *argc, **kwarg):
        super(BaseHandler, self).__init__(*argc, **kwarg)

    def get_current_user(self):
        return self.get_secure_cookie("user")
    '''
    def get(self):
        self.send_error(404)
    '''
    def mywrite(self, chunk):

        # 定义自己实现的write()方法
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if not isinstance(chunk, (list, dict)):
            message = "write() only accepts bytes, unicode, list and dict objects"
            raise TypeError(message)
        if isinstance(chunk, (list, dict)):
            chunk = json.dumps(chunk,cls=MyEncoder).replace("</", "<\\/")
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
        greeting = greeting + ',friendly user!'
        #self.mywrite([greeting.encode("utf8")])
        self.write(greeting)
    '''
    def get(self):

        code = self.get_argument('code')
        start = self.get_argument('start')
        mid = self.get_argument('mid') # linear_C的新参数
        end = self.get_argument('end')

        #db = linear_B(code,start,end)
        #new_pointup, new_point_low = linear_C(code, start, mid, end)
        new_pointup = get_http_data.read_trend_txt()
        db = json.dumps(new_pointup) 
        self.write(db)
        #self.mywrite(new_pointup)
    
if __name__== "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/",IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()