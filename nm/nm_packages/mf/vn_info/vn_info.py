from vn_node import VNNode
import xml.etree.ElementTree as ET
import sys

__author__="wontoniii"


class VNInfo:
    """

    """

    def __init__(self):
        """
        Initialize empty VN
        """
        self.vnGuid = 0
        self.owner = 0
        self.nodes = {}
        self.services = {}

    def copyInfo(self, vninfo):
        """
        Initialize VN from other VNInfo instance
        TODO
        :param vnGuid:
        """
        self.vnGuid = vninfo.vnGuid
        for key,value in vninfo:
            self.nodes[key] = VNNode(value)

    def loadFromXmlFile(self, filename):
        """
        Load VNInfo from XML file
        :param filename:
        :return:
        """
        tree = ET.parse(filename)
        self.loadXml(tree)

    def loadFromXmlString(self, string):
        """
        Load VNInfo from XML string
        :param string:
        :return:
        """
        tree = ET.fromstring(string)
        self.loadXml(tree)

    def loadXml(self, tree):
        root = tree.getroot()
        if root.tag != "topology":
            return
        for child in root:
            if child.tag == "vnguid":
                self.vnGuid = child.attrib['guid']
            elif child.tag == "owner":
                self.owner = child.attrib['guid']
            elif child.tag == "node":
                node = VNNode()
                node.loadFromXmlElement(child)
                self.nodes[node.vguid] = node
            elif child.tag == "service_map":
                self.services[child.attrib['guid']] = []
                for member in child:
                    if member.tag == "member":
                        self.services[child.attrib['guid']].append(member.attrib['guid'])
                    else:
                        print "Invalid tag " + member.tag
            else:
                print "Invalid tag " + child.tag

    def createVTopologyString(self, stringformat = "default"):
        """
        Returns the topology string used by the click router to initialize a VN.
        If format is "click" it adds punctuation used in the write handler
        :return: the generated string
        """
        topology = ""
        i = 0
        for node in self.nodes.values():
            if i > 0:
                if stringformat == "click":
                    topology += ","
                else:
                    topology += "\n"
            i += 1
            topology = topology + node.vguid + " " + str(len(node.neighbors))
            for neighbor in node.neighbors:
                topology = topology + " " + neighbor
        if stringformat == "click":
            topology += ":"
        return topology

    def createVServiceString(self, stringformat = "default"):
        """
        Returns the service string used by the click router to initialize a VN.
        If format is "click" it adds punctuation used in the write handler
        :return: the generated string
        """
        sstring = ""
        i = 0
        for key, members in self.services.iteritems():
            if i > 0:
                if stringformat == "click":
                    sstring += ","
                else:
                    sstring += "\n"
            i += 1
            sstring = sstring + key + " " + str(len(members))
            for value in members:
                sstring = sstring + " " + value

        if stringformat == "click":
            sstring += ":"
        return sstring

    def createGuidsString(self, stringformat = "default"):
        """
        Returns the guids string used by the click router to initialize a VN.
        If format is "click" it adds punctuation used in the write handler
        :return: the generated string
        """
        topology = "num_nodes " + str(len(self.nodes))
        if stringformat == "click":
            topology += ","
        else:
            topology += "\n"
        for node in self.nodes.values():
            topology = topology + node.vguid + " " + node.guid
            if stringformat == "click":
                topology += ","
            else:
                topology += "\n"
        if stringformat == "click":
            topology += ":"
        return topology

    def createXMLForNode(self, nodeguid):
        """

        :return:
        """
        root = ET.Element("topology")
        owner = ET.SubElement(root, "owner", {"guid": nodeguid})
        vnguid = ET.SubElement(root, "vnguid", {"guid": self.vnGuid})
        for node in self.nodes.values():
            xmlnode = ET.SubElement(root, "node", {"guid": node.guid, "vguid": node.vguid})
            for neighbor in node.neighbors:
                ET.SubElement(xmlnode, "neighbor", {"guid": neighbor})
        for serviceid, members in self.services.iteritems():
            xmlnode = ET.SubElement(root, "service_map", {"guid": serviceid})
            for service in members:
                ET.SubElement(xmlnode, "member", {"guid": service})
        return ET.tostring(root)


if __name__ == "__main__":
    vninfo = VNInfo()
    vninfo.loadFromXmlFile(sys.argv[1])
    print vninfo.createGuidsString()
    print "\n"
    print vninfo.createVServiceString()
    print "\n"
    print vninfo.createVTopologyString()
    print "\n"
    print vninfo.createXMLForNode(sys.argv[2])
