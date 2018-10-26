from nm.nm_functions.periodic_event import PeriodicThread
import time

__author__ = "wontoniii"


class TimeoutEvent(PeriodicThread):
  """

  """

  def __init__(self, callbackObject, args, threadID, period):
    PeriodicThread.__init__(self, callbackObject, args, threadID, period)
    self.rescheduleTime = 0
    self.rescheduled = False

  def run(self):
    print "Starting periodic task for class" + self.callbackObject.__str__()
    self.rescheduleTime = time.time()
    self.rescheduled = True
    while self.running is True:
      if self.rescheduled and self.running:
        self.rescheduled = False
        currentTime = time.time()
        sleepTime = self.period - (self.rescheduleTime - currentTime)
        time.sleep(sleepTime)
      else:
        self.running = False
        self.callbackObject.callback(self.threadID, self.args)

  def stop(self):
    self.running = False

  def reschedule(self):
    """
    Restart timer
    :return:
    """
    self.rescheduled = True
    self.rescheduleTime = time.time()
