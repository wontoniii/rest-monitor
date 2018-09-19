import service
from nm_functions.timeoutEvent import TimeoutEvent
from nm_node import NMNode

__author__ = "wontoniii"


class VNCentralService (service.Service):
    """

    """

    def __init__(self, nmsystem):
        super(VNCentralService, self).__init__(nmsystem)
        self.section = "VN_CENTRAL_SERVICE"

    def start(self):
        """
        Just start periodic printing of something dummy
        :return:
        """
        to = TimeoutEvent(self, None, 0, self.config['INITIAL_TIMEOUT'])
        to.run()


    def stop(self):
        """
        Stop eventual service components
        :return:
        """
        pass

    def loadConfig(self, config_parser, section = None):
        """
        Temp
        :param self:
        :param config:
        :param section:
        :return:
        """
        for k in config_parser.options(self.section):
            if k in ['INITIAL_TIMEOUT']:
                self.config[k] = config_parser.gettime(self.section, k)
            elif k in ['VN_TOPOLOGIES']:
                self.config[k] = config_parser.getstringlist(section, k)
            else:
                self.config[k] = config_parser.get(self.section, k)

    def callback(self, threadID, args):
        """
        Periodically pull data from click and store it somewhere
        :return:
        """
        print "Expired TO for node with guid: " + threadID

    def handleStartTO(self):
        """

        :return:
        """
        # TODO: read all VN files and start their TOs

    def handleVNTO(self, VNID):
        """

        :param VNID:
        :return:
        """
        # TODO: Start VN by sending HTTP POST to all participating routers
        # TODO: If not all VN nodes are up waits to initialize it
