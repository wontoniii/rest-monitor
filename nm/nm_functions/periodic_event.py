import threading
import time

__author__ = "wontoniii"


class PeriodicThread(threading.Thread):
  """
  Class that handles periodic threads
  """

  def __init__(self, callbackObject, args, threadID, period):
    threading.Thread.__init__(self)
    self.callbackObject = callbackObject
    self.period = period
    self.args = args
    self.threadID = threadID
    self.running = True

  def run(self):
    print "Starting periodic task for class" + self.callbackObject.__str__()
    while self.running is True:
      time.sleep(self.period)
      self.callbackObject.callback(self.threadID, self.args)

  def stop(self):
    self.running = False
