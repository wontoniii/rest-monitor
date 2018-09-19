__author__ = "wontoniii"


class VNNode:
    """

    """

    def __init__(self):
        """
        Initiate empty node
        """
        self.guid = 0
        self.vguid = 0
        self.neighbors = []

    def copyNode(self, vnnode):
        """
        TODO
        """
        self.guid = vnnode.guid
        self.vguid = vnnode.vguid

    def loadFromXmlElement(self, element):
        """

        :param element:
        :return:
        """
        # TODO: check errors
        self.guid = element.attrib['guid']
        self.vguid = element.attrib['vguid']
        for child in element:
            if child.tag == "neighbor":
                self.neighbors.append(child.attrib['guid'])
            else:
                print "Invalid tag " + child.tag