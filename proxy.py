from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = '192.168.56.1'
PORT = 8000


class Proxy(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes('<html><body><h1>Hi!</h1></body></html>', 'utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes('<html><body><h1>Hi!</h1></body></html>', 'utf-8'))


server = HTTPServer((HOST, PORT), Proxy)
print('Server is running...')
server.serve_forever()
server.server_close()
