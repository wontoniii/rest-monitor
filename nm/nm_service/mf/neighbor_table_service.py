import service
import json
from nm_functions.periodicEvent import PeriodicThread

__author__ = "wontoniii"


class NeighborTableService (service.Service):
    """

    """

    def __init__(self, nmsystem):
        super(NeighborTableService, self).__init__(nmsystem)
        self.thread = PeriodicThread(self, None, 1, 5)
        self.section = "NEIGHBOR_SERVICE_TABLE"

    def start(self):
        """
        Just start periodic printing of something dummy
        :return:
        """
        self.thread.period = self.config['PERIOD']
        self.thread.start()

    def stop(self):
        """
        Stop eventual service components
        :return:
        """
        print "Stopping thread"
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
        print "This functional should create a json or xml representation of the neighbors list"
        return [True, None, "No neighbors"]


    def pullClickData(self):
        self.system.socket.sendCommand("read nbr_tbl.neighbor_table\n")
        data = self.system.socket.receiveData(100)
        print "Pulled data from Click:\n" + data

        # format the data as a list
        format_data = []
        words = data.split(';')
        for item in words:
            if len(item) > 2:
                item = item[1:-1]
                elems = item.split(',')
                neigb = {}
                neigb['GUID'] = int(elems[0])
                neigb['s_ett'] = int(elems[1])
                neigb['l_ett'] = int(elems[2])
                format_data.append(neigb)

        return format_data

    def callback(self, threadID, args):
        """
        Periodically pull data from click and store it somewhere
        :return:
        """
        print "Performing periodic task"
        # pullClickData()
