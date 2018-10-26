import service
import subprocess

__author__ = "wontoniii"


class PingerService (service.Service):

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

  def launchPing(self, count=1, interval=.100, destination="127.0.0.1", output_file="PingLog.log"):
    """

    Method to receive parameters to launch ping to destination host

    It will return success or fail based on ping execution, if it was possible to be triggered
    it is a success if not, fail and include the error.
    :param count:
    :param interval:
    :param destination:
    :param output_file:
    :return:
    """

    print "Function to Launch Ping"
    successful_result = True

    ping_command = "ping -c " + str(count) + " -i " + str(
      interval) + " " + destination + " > ./" + output_file

    # try:
    #   # Process completed successfully, zero value returned
    #   subprocess.check_call(ping_command)
    # except subprocess.CalledProcessError:
    #   # Error presented, non-zero value has been returned
    #   successful_result = False

    console_output, error = subprocess.Popen(ping_command,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True).communicate()
    print console_output, error

    if error:
      successful_result = False


    return successful_result

  def handleGetRequest(self, path_components, query_components):
    """
    Handle service get request
    :param path:
    :param parameters:
    :return:
    """

    count = query_components['count'][0]
    dest = query_components['dest'][0]
    interval = query_components['interval'][0]
    outfile = query_components['outfile'][0]

    # print "Count: "+str(count)
    # print "Interval: " + str(interval)
    # print "Destination: " + str(dest)
    # print "Output File: " + str(outfile)


    if self.launchPing(count, interval, dest, outfile):
      print "Log file has been succesfully created."
    else:
      print "Error while processing the ping command."


    print "Debug of Pinger service:"
    print "\tPath components: " + str(path_components)
    print "\tQuery components " + str(query_components)
    return [True, None, "PingerService"]
