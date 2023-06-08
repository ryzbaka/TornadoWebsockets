import tornado.web
import tornado.websocket
import tornado.ioloop
import yaml

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        client_id = self.get_argument("client_id",default=None)
        print(f"Connection opened to {client_id}")
        self.connections.add(self)
    
    def on_message(self,message):
        data = yaml.safe_load(message)
        print(data)
        for conn in self.connections:
            conn.write_message(f"{data['sender']}: {data['message']} ")
    def on_close(self):
        self.connections.remove(self)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

app = tornado.web.Application([
    (r"/",MainHandler),
    (r"/ws",WebSocketHandler),
])

if __name__=="__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()