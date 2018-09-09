#!/usr/bin/env python
 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Predictive model data goes here"
        # Send message back to client
        print(message)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('10.142.0.2', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()