from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import direct.directbase.DirectStart
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
import sys

import config
from gamelogic import GameLogic

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

        self.gameLogic = GameLogic()

        blackmaker = CardMaker("blackmaker")
        blackmaker.setColor(0,0,0,1)
        blackmaker.setFrame(-1.0, 1.0, -1.0, 1.0)
        instcard = NodePath(blackmaker.generate())
        instcard.reparentTo(render2d)

        self.screenText = OnscreenText(text="Server started ...\n",
            style=1, fg=(1,1,1,1), pos=(-1.31, 0.925), scale = .06)
        self.screenText.setAlign(0)

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
                self.screenText.appendText("New connection established.\n")
            else: 
                self.screenText.appendText("getNewConnection returned false\n")
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
            self.screenText.appendText("Unknown msgID: ")
            self.screenText.appendText(msgID)
            self.screenText.appendText("\n")
            self.screenText.appendText(data)
            self.screenText.appendText("\n")
        return

    ######################################################################################

    def msgAuth(self, msgID, data, client):
        name = data.getString()
        CLIENTS[client] = name
        pkg = PyDatagram()
        pkg.addUint16(config.SV_MSG_AUTH_RESPONSE)
        self.cWriter.send(pkg, client)
        self.screenText.appendText("Registered new client: ")
        self.screenText.appendText(name)
        self.screenText.appendText(" (")
        self.screenText.appendText(client.getAddress().getIpString())
        self.screenText.appendText(")\n")

    ######################################################################################

    def msgChat(self, msgID, data, senderClient):
        message = data.getString()
        self.screenText.appendText("Message: ")
        self.screenText.appendText(message)
        self.screenText.appendText("\n")
        pkg = PyDatagram()
        pkg.addUint16(config.SV_MSG_CHAT)
        pkg.addString(message)
        for receiverClient in CLIENTS:
            self.cWriter.send(pkg, receiverClient)

    ######################################################################################

    def msgDisconnectReq(self, msgID, data, client): 
        pkg = PyDatagram() 
        pkg.addUint16(config.SV_MSG_DISCONNECT_ACK) 
        self.cWriter.send(pkg, client) 
        del CLIENTS[client]
        self.cReader.removeConnection(client)

    ######################################################################################

    def handleCompleteSetup(self, msgID, data, senderClient):
        self.screenText.appendText("A new game will start... ")
        self.screenText.appendText(str(len(CLIENTS)))
        self.screenText.appendText(" pushies will fight to death.")
        self.gameLogic.start()
        pkg = PyDatagram()
        pkg.addUint16(config.SV_MSG_START_GAME)
        pkg.addUint16(len(CLIENTS))
        for receiverClient in CLIENTS:    
            self.cWriter.send(pkg, receiverClient)

    ######################################################################################

    def handlePerformWalk(self, msgID, data, client):
        player = CLIENTS[client]
        direction = data.getUInt8()

    def handlePerformClout(self, msgID, data, client):
        player = CLIENTS[client]

    def handlePerformJump(self, msgID, data, client):
        player = CLIENTS[client]

    def handlePerformCharge(self, msgID, data, client):
        player = CLIENTS[client]

    ######################################################################################

    def handleCompleteWalk(self, msgID, data, client):
        player = CLIENTS[client]

    def handleCompleteJump(self, msgID, data, client):
        player = CLIENTS[client]

    def handleCompleteCharge(self, msgID, data, client):
        player = CLIENTS[client]

    ######################################################################################

    def quit(self): 
        self.cManager.closeConnection(self.tcpSocket) 
        sys.exit() 

# create a server object on port 9099 
server = Server() 

#install msg handlers 
Handlers = { 
    config.CL_MSG_AUTH              : server.msgAuth, 
    config.CL_MSG_CHAT              : server.msgChat, 
    config.CL_MSG_DISCONNECT_REQ    : server.msgDisconnectReq,
    config.CL_MSG_COMPLETE_SETUP    : server.handleCompleteSetup,
    config.CL_MSG_PERFORM_WALK      : server.handlePerformWalk,
    config.CL_MSG_PERFORM_CLOUT     : server.handlePerformClout,
    config.CL_MSG_PERFORM_JUMP      : server.handlePerformJump,
    config.CL_MSG_PERFORM_CHARGE    : server.handlePerformCharge,
    config.CL_MSG_COMPLETE_WALK     : server.handleCompleteWalk,
    config.CL_MSG_COMPLETE_JUMP     : server.handleCompleteJump,
    config.CL_MSG_COMPLETE_CHARGE   : server.handleCompleteCharge
    } 

run()