from http.server import BaseHTTPRequestHandler, HTTPServer
from hello import hello
from restaurant import restaurantHandler;
from restaurantui import restaurantUI;

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            
            if self.path.endswith("/hello"):
                hello.doGet(self)

            if self.path.endswith("/hola"):
                hello.doGetHola(self)

            if self.path.endswith("/restaurants"):
                restaurantUI.doGet(self)
            
            if self.path.endswith("/new"):
                restaurantUI.newPage(self)

            if self.path.endswith("/edit"):
                restaurantUI.editPage(self)

            if self.path.endswith("/delete"):
                restaurantUI.deletePage(self)

        except Exception as e:
            print(e)
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                hello.doPost(self)
            
            if self.path.endswith("/new"):
                restaurantHandler.add(self)

            if self.path.endswith("/doEdit"):
                restaurantHandler.update(self)

            if self.path.endswith("/delete"):
                restaurantHandler.delete(self)

        except Exception as e:
            print(e)
            self.send_error(500, e)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()
    
    except KeyboardInterrupt:
        print("^C entedered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()