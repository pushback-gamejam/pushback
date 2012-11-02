from pandac.PandaModules import * 
from direct.showbase.ShowBase import ShowBase
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectGui import *
from direct.task import Task
import sys

import config

class Client(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape", self.sendMsgDisconnectReq)
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.Connection = self.cManager.openTCPClientConnection(config.SERVER_IP, config.SERVER_PORT, 1)
        self.cReader.addConnection(self.Connection)
        taskMgr.add(self.readTask, "serverReaderPollTask", -39)
        self.sendMsgAuth()

    ######################################################################################

    def readTask(self, task):
        while 1:
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader) 
            if msgID is config.MSG_NONE:
                break 
            else:
                self.handleDatagram(data, msgID)
        return Task.cont 

    ######################################################################################

    def nonBlockingRead(self,qcr): 
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

    def handleDatagram(self, data, msgID):      
        if msgID in Handlers.keys(): 
            Handlers[msgID](msgID, data) 
        else: 
            print "Unknown msgID: %d" % msgID 
            print data 
        return        

    ######################################################################################

    def sendMsgAuth(self):
        pkg = PyDatagram()
        pkg.addUint16(config.CL_MSG_AUTH) 
        self.send(pkg)

    ######################################################################################

    def msgAuthResponse(self, msgID, data): 
        pkg = PyDatagram()
        pkg.addUint16(config.CL_MSG_CHAT)
        pkg.addString("client is calling in and is glad to be here")
        self.send(pkg)

    ######################################################################################

    def sendMsgDisconnectReq(self): 
        pkg = PyDatagram() 
        pkg.addUint16(config.CL_MSG_DISCONNECT_REQ) 
        self.send(pkg) 

    ######################################################################################

    def msgChat(self, msgID, data):
        print data.getString() 

    ######################################################################################

    def msgDisconnectAck(self, msgID, data):  
        self.cManager.closeConnection(self.Connection)  
        sys.exit() 

    ######################################################################################

    def send(self, pkg):
        self.cWriter.send(pkg, self.Connection) 

    ######################################################################################

    def quit(self): 
        self.cManager.closeConnection(self.Connection) 
        sys.exit() 

client = Client() 

Handlers = { 
    config.SV_MSG_AUTH_RESPONSE  : client.msgAuthResponse, 
    config.SV_MSG_CHAT           : client.msgChat, 
    config.SV_MSG_DISCONNECT_ACK : client.msgDisconnectAck, 
    } 

run()