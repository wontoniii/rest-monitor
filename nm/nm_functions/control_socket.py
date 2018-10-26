from socket import socket
from threading import Lock


class ControlSocket(socket):
  """
      Implements communication tool with Click control port
  """

  def __init__(self):
    """
    Overload init to initialize with preconfigured values
    """
    super(ControlSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self, host, port):
    """
    Connects to Click interface
    :param host:
    :param port:
    :return:
    """
    self.connect((host, port))
    # discard initial message from click
    response = self.recv(1024)
    print "Initial click response: " + response

  def sendData(self, data):
    """
    :param data:
    :return:
    """
    byte_sent = self.send(data)
    if byte_sent < len(data):
      print "Not all data is sent out!"
    return byte_sent

  def receiveData(self, buf_length):
    buf = self.recv(buf_length)
    # TODO Handle 3 lines
    return buf

  def sendCommand(self, cmd, responseLenght = 0):
    """
    :param cmd:
    :return:
    """
    self.sendData(cmd)
    if responseLenght > 0:
      return self.receiveData(responseLenght)
    else:
      return 0


class ConcurrentControlSocket(ControlSocket):
  """
      Implements communication tool with Click control port
  """

  def __init__(self):
    """
    Overload init to initialize with preconfigured values
    """
    super(ConcurrentControlSocket, self).__init__()
    self.lock = Lock()

  def sendCommand(self, cmd, responseLenght = 0):
    """
    :param cmd:
    :return:
    """
    self.lock.acquire()
    self.sendData(cmd)
    returned = 0
    if responseLenght > 0:
      returned = self.receiveData(responseLenght)
    self.lock.release()
    return returned
