import service

__author__ = "wontoniii"


class DummyService (service.Service):

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
    pass

  def handleGetRequest(self, path_components, query_components):
    """
    Handle service get request
    :param path:
    :param parameters:
    :return:
    """
    print "I'm dummy, not doing anything with request:"
    print "\tPath components: " + str(path_components)
    print "\tQuery components " + str(query_components)
    return [True, None, "Dummy Service"]
