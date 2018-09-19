import nm.nm_service.service as service
from nm.nm_packages.mf.vn_info.vn_info import VNInfo

__author__ = "wontoniii"


class VNLocalService (service.Service):
    """

    """

    def __init__(self, nmsystem):
        super(VNLocalService, self).__init__(nmsystem)
        self.section = "VN_LOCAL_SERVICE"

    def handlePostRequest(self, path_components, query_components, body):
        """

        :param path_components:
        :param query_components:
        :param body: contains the VN xml file
        :return:
        """
        # TODO implement error checking
        vninfo = VNInfo()
        vninfo.loadFromXmlString(body)
        # TODO check it's the right order
        clickString = vninfo.createVTopologyString(stringformat="click")\
                      + vninfo.createVServiceString(stringformat="click")\
                      + vninfo.createGuidsString(stringformat="click")
        self.system.socket.sendCommand("write MF_VNDynamicLoader.add " + clickString + "\n")
        return [True, None, "VN Initialized"]
