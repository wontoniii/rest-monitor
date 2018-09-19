import nm.nm_service.service as service
from nm.nm_functions.timeout_event import TimeoutEvent
from nm.nm_node import NMNode

__author__ = "wontoniii"


class TopologyService (service.Service):
    """

    """

    def __init__(self, nmsystem):
        super(TopologyService, self).__init__(nmsystem)
        # self.thread = PeriodicThread(self, None, 1, 5)
        self.tos = {}
        self.nodes = {}
        self.section = "TOPOLOGY_SERVICE"

    def start(self):
        """
        Just start periodic printing of something dummy
        :return:
        """

    def stop(self):
        """
        Stop eventual service components
        :return:
        """
        print "Stopping threads"
        for thread in self.tos.values():
            thread.stop()
            thread.join(self.config['TIMEOUT'] + 1)

    def loadConfig(self, config_parser, section = None):
        """
        Temp
        :param self:
        :param config:
        :param section:
        :return:
        """
        for k in config_parser.options(self.section):
            if k in ['TIMEOUT']:
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
        try:
            guid = query_components['guid'][0]
            if guid in self.nodes.keys():
                self.tos[guid].reschedule()
            else:
                node = NMNode()
                node.guid = query_components['guid'][0]
                node.ip = query_components['ip'][0]
                node.port = query_components['port'][0]
                self.nodes[node.guid] = node
                self.tos[node.guid] = TimeoutEvent(self, None, node.guid, self.config['TIMEOUT'])
                self.tos[node.guid].start()
        except KeyError:
            print "Missing parameter in " + str(query_components)
            return [True, None, "Missing Required Parameter"]
        return [True, None, "Registered"]

    def callback(self, threadID, args):
        """
        Periodically pull data from click and store it somewhere
        :return:
        """
        print "Expired TO for node with guid: " + threadID
        self.tos[threadID].stop()
        del self.tos[threadID]
        del self.nodes[threadID]

    def topologyContains(self, nodesList):
        """
        Check if list of guids has registered already
        :param nodesList:
        :return: returns Trus if contains all, False otherwise
        """
        for node in nodesList:
            if node not in self.nodes.keys():
                return False
        return True
