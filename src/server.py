from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import direct.directbase.DirectStart
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
import sys

from config import *
from defines import *
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
        self.tcpSocket = self.cManager.openTCPServerRendezvous(SERVER_PORT, 1)
        self.cListener.addConnection(self.tcpSocket)
        taskMgr.add(self.listenTask, "serverListenTask", -40)
        taskMgr.add(self.readTask, "serverReadTask", -39)

        self.gameLogic = GameLogic()
        self.gameLogic.delegate = self;

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
            if msgID is MSG_NONE: 
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
                msgID = MSG_NONE 
        else: 
            datagram = None 
            data = None 
            msgID = MSG_NONE 
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
        self.gameLogic.addPlayer(name)
        pkg = PyDatagram()
        pkg.addUint16(SV_MSG_AUTH_RESPONSE)
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
        pkg.addUint16(SV_MSG_CHAT)
        pkg.addString(message)
        for receiverClient in CLIENTS:
            self.cWriter.send(pkg, receiverClient)

    ######################################################################################

    def msgDisconnectReq(self, msgID, data, client): 
        pkg = PyDatagram() 
        pkg.addUint16(SV_MSG_DISCONNECT_ACK) 
        self.cWriter.send(pkg, client) 
        del CLIENTS[client]
        self.cReader.removeConnection(client)

    ######################################################################################

    def handleCompleteSetup(self, msgID, data, senderClient):
        self.screenText.appendText("A new game will start... ")
        self.screenText.appendText(str(len(CLIENTS)))
        self.screenText.appendText(" pushies will fight to death.")
        setups = self.gameLogic.start()
        numberOfPlayers = len(setups)
        pkg = PyDatagram()
        pkg.addUint16(SV_MSG_START_GAME)
        pkg.addUint16(numberOfPlayers)
        for setup in setups:
            pkg.addString(setup["player"])
            pkg.addFloat32(setup["position"][0])
            pkg.addFloat32(setup["position"][1])
            pkg.addFloat32(setup["position"][2])
        for receiverClient in CLIENTS:    
            self.cWriter.send(pkg, receiverClient)

    ######################################################################################

    def handleMovementCommand(self, msgID, data, client):
        player = CLIENTS[client]
        movement = data.getUint8()
        status = data.getUint8()
        self.gameLogic.setPlayerMovement(player, movement, status)

    def handleJumpCommand(self, msgID, data, client):
        player = CLIENTS[client]
        status = data.getUint8()
        self.gameLogic.setPlayerJump(player, status)

    def handleChargeCommand(self, msgID, data, client):
        player = CLIENTS[client]
        status = data.getUint8()
        self.gameLogic.setPlayerCharge(player, status)

    ######################################################################################

    def sendPositionUpdates(self, updates):
        pkg = PyDatagram()
        pkg.addUint16(SV_MSG_UPDATE_POSITIONS)
        pkg.addUint16(len(updates))
        for update in updates:
            pkg.addString(update[0])
            pkg.addFloat32(update[1][0])
            pkg.addFloat32(update[1][1])
            pkg.addFloat32(update[1][2])
            pkg.addFloat32(update[2][0])
            pkg.addFloat32(update[2][1])
            pkg.addFloat32(update[2][2])
        for client in CLIENTS:
            self.cWriter.send(pkg, client)
        #print "Sent position updates to %d clients." % len(CLIENTS)

    def sendStatusUpdates(self, updates):
        pkg = PyDatagram()
        pkg.addUint16(SV_MSG_UPDATE_STATES)
        pkg.addUint16(len(updates))
        for update in updates:
            pkg.addString(update["player"])
            pkg.addUint8(update["status"])
            pkg.addFloat32(update["health"])
            pkg.addUint8(update["charge"])
            pkg.addUint8(update["jump"])
        for client in CLIENTS:
            self.cWriter.send(pkg, client)

    def quit(self): 
        self.cManager.closeConnection(self.tcpSocket) 
        sys.exit() 

server = Server() 

Handlers = { 
    CL_MSG_AUTH              : server.msgAuth, 
    CL_MSG_CHAT              : server.msgChat, 
    CL_MSG_DISCONNECT_REQ    : server.msgDisconnectReq,
    CL_MSG_COMPLETE_SETUP    : server.handleCompleteSetup,
    CL_MSG_MOVEMENT_COMMAND  : server.handleMovementCommand,
    CL_MSG_JUMP_COMMAND      : server.handleJumpCommand,
    CL_MSG_CHARGE_COMMAND    : server.handleChargeCommand
    } 

run()
