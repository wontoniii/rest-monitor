import time
import httplib
import socket
import sys
import random

__author__="wontoniii"

HTTP_ERROR_CODES = [400, 401, 402, 403, 404, 500, 501, 502, 503]
HTTP_SUCCESS_CODES = [200]


class HttpClient:
    """
    HTTP client that sequentially request a list of files
    """

    def __init__(self, destinationHost, localTO=0, socketTO=0, maxAttempts=1, files=None, debug=False):
        """
            * files: list of files
        """
        self.files = files
        self.dhost = destinationHost
        self.localTO = localTO
        self.socketTO = socketTO
        self.maxAttempts = maxAttempts
        self.debug = debug
        if self.debug:
            print "Parameters ", self.files, " ", self.dhost, " ", self.localTO, " ", self.socketTO

    def reliableHTTPRequest(self, method, URL, body = None):
        """
            Performs an HTTP request. Keeps looping until either the content is retrieved or the server returs an error
        """
        code = 0
        attempts = 0
        data = None
        while code not in HTTP_ERROR_CODES and code not in HTTP_SUCCESS_CODES and attempts < self.maxAttempts:
            attempts += 1
            if self.debug:
                print "Retrieving: ", self.dhost, URL

            try:
                if self.socketTO > 0:
                    conn = httplib.HTTPConnection(self.dhost, timeout=self.socketTO)
                else:
                    conn = httplib.HTTPConnection(self.dhost)
                conn.request(method, URL, body)
                response = conn.getresponse()
                if response.status in HTTP_SUCCESS_CODES:
                    if self.debug:
                        print "Received success status: ", response.status, "\nResponse:", response.reason
                    data = response.read()
                    if self.debug:
                        length = response.getheader("Content-Length")
                        print "Response size: ", length
                elif response.status in HTTP_ERROR_CODES:
                    if self.debug:
                        print "Received error status: ", response.status, "\nResponse:", response.reason
                else:
                    if self.debug:
                        print "Retrying in: ", self.localTO
                    time.sleep(self.to)
                conn.close()
                break
            except (httplib.HTTPException, socket.error) as e:
                if self.debug:
                    print "Exception: ", e
                    print "Retrying in: ", self.localTO
                time.sleep(self.localTO)
        return data


    def retriveMultipleFiles(self, files=None):
        """
            Sequentially request files
        """
        if files is not None:
            fileList = files
        elif self.files is not None:
            fileList = self.files
        else:
            return
        for file in fileList:
            self.reliableHTTPRequest("GET", file)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc>1:
        stime = int(sys.argv[1])*random.random()
        time.sleep(stime)
    client = HttpClient("localhost:8080", localTO=1, debug=True)
    files = ["/index.html", "/something.html"]
    client.retriveMultipleFiles(files)