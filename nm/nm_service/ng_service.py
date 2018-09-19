__author__ = 'romi'
'''
Stores the network graph in an igraph format, by periodically querying the routers in the network
and returns the graph to the webserver when requested
'''
import httplib
import time
import socket
import json
import threading
import igraph
import sys
import io
import ast
from service import Service

class NGService(Service):
    """

    """
    def __init__(self,nnodes=0, queryInt=5, debug=False):
        super(NGService, self).__init__()
        self.nnodes = nnodes
        self.debug = debug
        self.queryInt=queryInt
        self.parameters=[]
        if self.debug:
            print("Parameters: nnodes = ", self.nnodes, "query interval = ", self.queryInt)
        with open('node_param.txt', 'r') as fin:
            for line in fin:
                self.parameters.append(line.rstrip())
        self.nodeGraph = igraph.Graph()
        self.nodeGraph.add_vertices(self.nnodes)
        if self.debug:
            print("parameters for each node: ")
            print self.parameters
        while(1):
          for n in range(0, self.nnodes):
            logFile = "log" + str(n) + ".json"
            inFile = "sample" + str(n) + ".json"
            self.service = QueryService('localhost:8080', localTO=1, debug=True)
            if self.debug:
                print "at node " + str(n)
            #threading.Timer(self.queryInt, self.service.executeTask('sample0.json')).start ()
            self.service.executeTask(inFile, logFile)
          self.updateGraph()
          time.sleep(int(self.queryInt))

    def updateGraph(self):
        ##remove all existing edges in the graph
        self.nodeGraph = igraph.Graph()
        self.nodeGraph.add_vertices(self.nnodes)
        self.nodeGraph.vs["guid"] = [None]*self.nnodes

        for n in range(0,self.nnodes):
            logFile = "log" + str(n) + ".json"
            json_data=open(logFile).read()
            data = json.loads(json_data)
            data_dict = ast.literal_eval(data)
            node_guid = data_dict["guid"]

            if int(node_guid) in self.nodeGraph.vs["guid"]:
                indx1=self.nodeGraph.vs["guid"].index(node_guid)
            else: #new node
                indx1=len(self.nodeGraph.vs["guid"])-self.nodeGraph.vs["guid"].count(None)
                self.nodeGraph.vs[indx1]["guid"] = node_guid
            for p in range(1,len(self.parameters)):
                if self.parameters[p] in data_dict:
                    self.nodeGraph.vs[indx1][self.parameters[p]] = data_dict[self.parameters[p]]
            n_list = data_dict["neighbors"]
            for i in range(0, len(n_list)):
                n_dict = n_list[i]
                n_guid = n_dict["guid"]
                if int(n_guid) in self.nodeGraph.vs["guid"]:
                    indx2 = self.nodeGraph.vs["guid"].index(n_guid)
                    if self.nodeGraph.are_connected(indx1, indx2) == False: #no edge b/w the two
                        self.nodeGraph.add_edges([(indx1,indx2)])
                else: #n_guid not in vs["guid"]
                    indx2=len(self.nodeGraph.vs["guid"])-self.nodeGraph.vs["guid"].count(None)
                    self.nodeGraph.vs[indx2]["guid"] = n_guid
                    self.nodeGraph.add_edges([(indx1,indx2)])
                for p in range(1,len(self.parameters)):
                    if self.parameters[p] in n_dict:
                        self.nodeGraph.vs[indx2][self.parameters[p]] = n_dict[self.parameters[p]]

                    if self.debug:
                        print igraph.summary(self.nodeGraph)
        #data = self.getJson()
        #print data

    def getJson(self, params=[]):
        if not params:  #no paramaters specified, send the entire graph
            data=""
            for n in range(0,self.nnodes):
                logFile = "log" + str(n) + ".json"
                json_data=open(logFile).read()
                data = data + json.loads(json_data)
            return json.dumps(data)
        '''
        data=""
        for v in self.nodeGraph.vs:
            if v["guid"] == None:
                continue
            else:
                data=data + str(v["guid"])
                att_list = v.attributes()
                for a in att_list:
                    data=data + str(v[a])
            data=data+ "\n"
        print data


       # with io.open('test.json', 'w', encoding='utf-8') as fout:

      '''


class QueryService():
    HTTP_ERROR_CODES = [400, 401, 402, 403, 404, 500, 501, 502, 503]
    HTTP_SUCCESS_CODES = [200]
    def __init__(self,destinationHost, localTO=0, socketTO=0, files=None, debug=False):
        self.files = files
        self.dhost = destinationHost
        self.localTO = localTO
        self.socketTO = socketTO
        self.debug = debug
        if self.debug:
            print("Parameters ", self.files, " ", self.dhost, " ", self.localTO, " ", self.socketTO)

    def executeTask(self,inFile, logFile):
        self.reliableHTTPRequest("GET", inFile, logFile)

    def reliableHTTPRequest(self, method, URL, logFile):
        code = 0
        while code not in self.HTTP_ERROR_CODES and code not in self.HTTP_SUCCESS_CODES:
            if self.debug:
                print("Retrieving from: ", self.dhost, URL, " and saving at ", logFile)
            try:
                if self.socketTO > 0:
                    conn = httplib.HTTPConnection(self.dhost, timeout=self.socketTO)
                else:
                    conn = httplib.HTTPConnection(self.dhost)
                conn.request(method, URL)
                response = conn.getresponse()
                if response.status in self.HTTP_SUCCESS_CODES:
                    if self.debug:
                        print("Received success status: ", response.status, "\nResponse:", response.reason)
                    data = response.read()
                    with io.open(logFile, 'w', encoding='utf-8') as fout:
                      json.dump(data.decode('latin-1'),fout, ensure_ascii=False)
                    if self.debug:
                        length = response.getheader("Content-Length")
                        print("Response size: ", length)
                elif response.status in self.HTTP_ERROR_CODES:
                    if self.debug:
                        print("Received error status: ", response.status, "\nResponse:", response.reason)
                    data = None
                else:
                    if self.debug:
                        print("Retrying in: ", self.localTO)
                    time.sleep(self.localTO)
                conn.close()
                break
            except(httplib.HTTPException,socket.error) as e:
                if self.debug:
                    print("Exception: ", e)
                    print("Retrying in: ", self.localTO)
                time.sleep(self.localTO)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc>1:
        nnodes= int(sys.argv[1])
    NGService(nnodes,debug=True)
