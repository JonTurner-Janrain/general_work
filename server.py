from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'Received GET request for {self.path}')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(f'Received POST request with body:\n{body.decode()}')

if __name__ == '__main__':
    server_address = ('', 7777)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Listening on port 7777')
    httpd.serve_forever()
