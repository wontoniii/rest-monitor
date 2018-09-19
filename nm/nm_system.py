__author__ = 'wontoniii'

from nm_functions.webserver import ServiceHTTPServer
from nm_functions.control_socket import ControlSocket
from nm_functions.config import ExtendedConfigParser


class NMSystem:
    """
        A container for the main NM System elements
    """

    def __init__(self, webserver, socket, config, node, services):
        """
            Initialize
        """
        self.server = webserver
        self.socket = socket
        self.config = config
        self.myNode = node
        self.services = services
