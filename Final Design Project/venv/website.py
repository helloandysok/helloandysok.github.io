from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyServer(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.path = '/index.html'

    def get_stuff(self):
        if self.path == '/':
            pass
        try:
            file_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_open = "File not found. "
            self.send_response(404)
        self.end_header()
        self.wfile.write(bytes(file_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8080), MyServer)
httpd.serve_forever()
