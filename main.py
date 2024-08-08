from http.server import BaseHTTPRequestHandler, HTTPServer
import time

HOST = "192.168.1.77"
PORT = 8000

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "<html><body>Hello, World! <b>Here is a GET response</body></html>"
        self.wfile.write(bytes(message, "utf8"))
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes('{"time": "' +  date + '"}', "utf8"))

    #def do_POST(self):
        #self.send_response(200)
        #self.send_header('Content-type','text/html')
        #self.end_headers()

        #message = "Hello, World! Here is a POST response"
        #self.wfile.write(bytes(message, "utf8"))

#with HTTPServer(('', 8000), handler) as server:
    #server.serve_forever()

server = HTTPServer((HOST, PORT), handler)
print("server now running...")
server.serve_forever()
server.server_close()
print("server stopped")