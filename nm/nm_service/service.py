__author__ = 'wontoniii'

from nm_system import NMSystem


class Service(object):
    """
        General class for all services.
        Implements common functionalities
    """

    def __init__(self, nmsystem):
        self.system = nmsystem
        self.config = {}

    def start(self):
        """
        Start eventual required service components
        :return:
        """
        print "start function not implemented for service"

    def stop(self):
        """
        Stop eventual service components
        :return:
        """
        print "stop function not implemented for service"

    def handleGetRequest(self, path_components, query_components):
        """
        Handle service get request
        :param path:
        :param parameters:
        :return:
        """
        print "handleGetRequest function not implemented for service"
        return [True, None, "GET handler not implemented"]

    def handlePostRequest(self, path_components, query_components, body):
        """
        Handle service post request
        :param path:
        :param parameters:
        :return:
        """
        print "handleGetRequest function not implemented for service"
        return [True, None, "GET handler not implemented"]

    def loadConfig(self, config_parser, section = None):
        """
        Temp
        :param self:
        :param config:
        :param section:
        :return:
        """
        if section is None:
            return None
        for k in config_parser.options(section):
            self.config[k] = config_parser.get(section, k)
