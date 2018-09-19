import nm.nm_service.service as service
from nm.nm_functions.periodic_event import PeriodicThread
from nm.nm_functions.webclient import HttpClient
from nm.nm_node import NMNode

__author__ = "wontoniii"


class AssocService (service.Service):
    """

    """

    def __init__(self, nmsystem):
        super(AssocService, self).__init__(nmsystem)
        self.thread = PeriodicThread(self, None, 1, 5)
        self.section = "ASSOC_SERVICE"

    def start(self):
        """
        Just start periodic printing of something dummy
        :return:
        """
        self.thread.period = self.config['PERIOD']
        self.thread.run()

    def stop(self):
        """
        Stop eventual service components
        :return:
        """
        print "Stopping threads"
        self.thread.stop()
        self.thread.join(self.config['PERIOD'] + 1)

    def loadConfig(self, config_parser, section = None):
        """
        Temp
        :param self:
        :param config:
        :param section:
        :return:
        """
        for k in config_parser.options(self.section):
            if k in ['PERIOD']:
                self.config[k] = config_parser.gettime(self.section, k)
            else:
                self.config[k] = config_parser.get(self.section, k)

    def handleGetRequest(self, path_components, query_components):
        """
        Handle service get request
        :param path:
        :param parameters:
        :return:
        """
        print "Received unexpected get request"
        return [True, None, "Unexpected"]

    def callback(self, threadID, args):
        """
        Periodically pull data from click and store it somewhere
        :return:
        """
        print "Registering to central service"
        url = "/TopologyService?guid=" + self.system.myNode.guid + "&ip=" + self.system.myNode.ip + "&port=" + self.system.myNode.port
        httpClient = HttpClient(self.config['CENTRAL_SERVICE_IP'] + ":" + self.config['CENTRAL_SERVICE_PORT'])
        print "Received: " + httpClient.reliableHTTPRequest("GET", url)
