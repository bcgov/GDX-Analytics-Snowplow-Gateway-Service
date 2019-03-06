from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Hello, world, I am changing!\n", "utf-8"))
        return

httpd = HTTPServer(('0.0.0.0', 8080), RequestHandler)
httpd.serve_forever()