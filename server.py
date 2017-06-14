#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import main
import urllib

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/plain')
        self.end_headers()
        # Send message back to client
        message = "The Python runner is working!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    length = int(self.headers['Content-Length'])
    print('before taking file , length is: ', length)
    # You now have a dictionary of the post data
    payload = self.rfile.read(length)
    print('doing file stuff')
    f = open('btlib/myalgorithm.py','w')
    f.write(payload.decode(encoding='UTF-8'))
    f.close()
    self.wfile.write(bytes(main.backtest_algorithm(), "utf8"))
    return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
