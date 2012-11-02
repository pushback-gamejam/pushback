from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import direct.directbase.DirectStart
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.gui.DirectGui import *
import sys

import config

CLIENTS = {} 

class Server(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.accept("escape", self.quit) 
        self.lastConnection = None 
        self.cManager = QueuedConnectionManager() 
        self.cListener = QueuedConnectionListener(self.cManager, 0) 
        self.cReader = QueuedConnectionReader(self.cManager, 0) 
        self.cWriter = ConnectionWriter(self.cManager,0) 
        self.tcpSocket = self.cManager.openTCPServerRendezvous(config.SERVER_PORT, 1) 
        self.cListener.addConnection(self.tcpSocket) 
        taskMgr.add(self.listenTask, "serverListenTask", -40) 
        taskMgr.add(self.readTask, "serverReadTask", -39) 

    ######################################################################################

    def listenTask(self, task):
        if self.cListener.newConnectionAvailable(): 
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                self.cReader.addConnection(newConnection)
                CLIENTS[newConnection] = netAddress.getIpString()
                self.lastConnection = newConnection
                print "Got a connection!"
            else: 
                print "getNewConnection returned false"
        return Task.cont 

    ######################################################################################

    def readTask(self, task):
        while 1: 
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader) 
            if msgID is config.MSG_NONE: 
                break 
            else:
                self.handleDatagram(data, msgID, datagram.getConnection()) 
        return Task.cont 

    ######################################################################################

    def nonBlockingRead(self, qcr): 
        if self.cReader.dataAvailable(): 
            datagram = NetDatagram() 
            if self.cReader.getData(datagram): 
                data = PyDatagramIterator(datagram) 
                msgID = data.getUint16() 
            else: 
                data = None 
                msgID = config.MSG_NONE 
        else: 
            datagram = None 
            data = None 
            msgID = config.MSG_NONE 
        return (datagram, data, msgID)

    ######################################################################################

    def handleDatagram(self, data, msgID, client): 
        if msgID in Handlers.keys():
            Handlers[msgID](msgID, data, client)
        else:
            print "Unknown msgID: %d" % msgID
            print data
        return

    ######################################################################################

    def msgAuth(self, msgID, data, client): 
        print "Registered new client: %s" % client.getAddress().getIpString()
        pkg = PyDatagram()
        pkg.addUint16(config.SV_MSG_AUTH_RESPONSE)
        self.cWriter.send(pkg, client)

    ######################################################################################

    def msgChat(self, msgID, data, senderClient):
        message = data.getString()
        print "ChatMsg: %s" % message
        for receiverClient in CLIENTS:
            pkg = PyDatagram()
            pkg.addUint16(config.SV_MSG_CHAT)
            pkg.addString(message)
            self.cWriter.send(pkg, receiverClient)

    ######################################################################################

    def msgDisconnectReq(self, msgID, data, client): 
        pkg = PyDatagram() 
        pkg.addUint16(config.SV_MSG_DISCONNECT_ACK) 
        self.cWriter.send(pkg, client) 
        del CLIENTS[client]
        self.cReader.removeConnection(client)

    ######################################################################################

    def quit(self): 
        self.cManager.closeConnection(self.tcpSocket) 
        sys.exit() 

# create a server object on port 9099 
serverHandler = Server() 

#install msg handlers 
Handlers = { 
    config.CL_MSG_AUTH           : serverHandler.msgAuth, 
    config.CL_MSG_CHAT           : serverHandler.msgChat, 
    config.CL_MSG_DISCONNECT_REQ : serverHandler.msgDisconnectReq, 
    } 

run()