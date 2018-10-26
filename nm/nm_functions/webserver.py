"""
    This module provide http interface for nm services
"""
__author__ = 'wontoniii'

import SimpleHTTPServer
import BaseHTTPServer
from urlparse import urlparse, parse_qs

from SocketServer import ThreadingMixIn
from nm.nm_service.ServiceException import ServiceNotFound


class ServiceHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    """
        Initialize the handler of the requests
    """
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

  def do_GET(self):
    """
        Handle a get request
    """
    try:
      parsed_query = urlparse(self.path)
      path_components = parsed_query.path.split("/")
      path_components = filter(None, path_components)
      query_components = parse_qs(parsed_query.query)
      [valid, headers, body] = self.server.callback.handleGetRequest(path_components, query_components)
      if valid is True:
        #send everything back
        self.send_response(200)
        if headers is not None:
          for key, value in headers.iteritems():
            self.send_header(key, value)
        self.end_headers()
        print "Sending " + body
        self.wfile.write(body)
      else:
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Service not running")
    except ServiceNotFound as e:
      #Send back error
      self.send_response(200)
      self.end_headers()
      self.wfile.write("Service not running")
    except Exception as general:
      print "Some other error: " + general.message
      self.send_response(200)
      self.end_headers()
      self.wfile.write("Service not running")

  def do_POST(self):
    """
        Handle a get request
    """
    try:
      parsed_query = urlparse(self.path)
      path_components = parsed_query.path.split("/")
      path_components = filter(None, path_components)
      query_components = parse_qs(parsed_query.query)
      # TODO: check how to avoid using the header
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      [valid, headers, body] = self.server.callback.handlePostRequest(path_components, query_components, post_body)
      if valid is True:
        # send everything back
        self.send_response(200)
        if headers is not None:
          for key, value in headers.iteritems():
            self.send_header(key, value)
        self.end_headers()
        print "Sending " + body
        self.wfile.write(body)
      else:
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Service not running")
    except ServiceNotFound as e:
      # Send back error
      self.send_response(200)
      self.end_headers()
      self.wfile.write("Service not running")
    except Exception as general:
      print "Some other error: " + general.message
      self.send_response(200)
      self.end_headers()
      self.wfile.write("Service not running")


class ServiceHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
  """
      Extend a normal python HTTP server. This will let us to manage various HTTP byte range requests
  """
  def __init__(self, serverAddress, handler, callback):
    BaseHTTPServer.HTTPServer.__init__(self, serverAddress, handler)
    self.callback = callback
