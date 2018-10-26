import importlib
from argparse import ArgumentParser
import signal
import sys

from nm_functions.config import ExtendedConfigParser
from nm_functions.webserver import ServiceHTTPServer,ServiceHTTPHandler
from nm_system import NMSystem
from nm_service.service_exception import ServiceNotFound
from nm_node import NMNode

__author__ = 'wontoniii'

#container for main object
nm = None

# Initialize the default config parameters
servicesAvailable = {"DummyService": getattr(importlib.import_module("nm_service.dummy"), "DummyService"),
                     "PingerService": getattr(importlib.import_module("nm_service.pinger"), "PingerService")}


def signal_handler(signal, frame):
  print('You pressed Ctrl+C! Gracefully exiting')
  if nm is not None:
    nm.cleanAll()
  sys.exit(0)


class NetworkMonitor:
  """
      Main class that initializes the NetworkMonitor
      Parses services and hosts
  """

  def __init__(self):
    """
    Initiate
    """
    self.system = None
    self.services = {}
    self.config = {}
    self.config_parser = None


  def run(self, confFile):
    config_parser = ExtendedConfigParser()
    config_parser.read(confFile)
    # TODO: Add control check for config file read correctly
    self.config = self.loadConfig(config_parser)
    if self.config["SERVER"] is True:
      server = self.initiateWebServer((self.config["SERVER_ADDRESS"],self.config["SERVER_PORT"]))
    else:
      server = None

    node = NMNode()
    node.guid = self.config["UID"]
    node.ip = self.config["SERVER_ADDRESS"]
    node.port = str(self.config["SERVER_PORT"])
    self.system = NMSystem(server, config_parser, node, self.services)
    self.initiateServices()
    server.serve_forever()


  def loadConfig(self, config_parser):
    """
    Temp
    :param self:
    :param config:
    :param section:
    :return:
    """
    section = "MAIN"
    config = {}
    for k in config_parser.options(section):
      if k in ['SERVER_PORT']:
        config[k] = config_parser.getint(section, k)
      elif k in []:
        config[k] = config_parser.gettime(section, k)
      elif k in ['SERVER']:
        config[k] = config_parser.getboolean(section, k)
      elif k in ['SERVICES']:
        config[k] = config_parser.getstringlist(section, k)
      # Everything else is a string
      else:
        config[k] = config_parser.get(section, k)
    return config


  def initiateWebServer(self, addr):
    """
    Initiates web server to list for requests
    :return:
    """
    print addr
    server = ServiceHTTPServer(addr, ServiceHTTPHandler, self)
    return server


  def initiateServices(self):
    """
    Initiates reqeusted services
    :return:
    """
    for service in self.config["SERVICES"]:
      print "Initiate service " + service
      if service in servicesAvailable:
        self.services[service] = servicesAvailable[service](self.system)
        self.services[service].loadConfig(self.system.config)
      else:
        print "Service", service, "not available"


  def startServices(self):
    for s in self.services.values():
      s.start()


  def handleGetRequest(self, path_components, query_components):
    """
    Handles get requests from web server
    If belongs to running service dispatches it
    :return:
    """
    print "Handling get request"
    if path_components[0] not in self.services.keys():
      print path_components[0] + " not running"
      raise ServiceNotFound(None)
    else:
      return self.services[path_components[0]].handleGetRequest(path_components, query_components)


  def handlePostRequest(self, path_components, query_components, body):
    """
    Handles oist requests from web server
    If belongs to running service dispatches it
    :return:
    """
    print "Handling get request"
    if path_components[0] not in self.services.keys():
      print path_components[0] + " not running"
      raise ServiceNotFound(None)
    else:
      return self.services[path_components[0]].handleGetRequest(path_components, query_components, body)


  def cleanAll(self):
    """
    Clean all running services and resources
    :return:
    """
    for s in self.services.values():
      s.stop()


def get_args():
  parser = ArgumentParser(description="MobilityFirst Service Monitor")
  parser.add_argument('--config_file', '-c',
                      type=str,
                      required=False,
                      help="Config file location",
                      default=".config",
                      dest="conf")
  parser.add_argument('-u', '--uid',
                      type=int,
                      required=False,
                      help="unique id to indentify node. If not specified uses the value from the config file")

  return parser.parse_args()


if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  args = get_args()
  nm = NetworkMonitor()
  nm.run(args.conf)