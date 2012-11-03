from pandac.PandaModules import * 
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.distributed.PyDatagram import PyDatagram 
from direct.distributed.PyDatagramIterator import PyDatagramIterator 
from direct.gui.DirectGui import *
from direct.task import Task
import sys

from config import *
from defines import *
#from gameoutput import GameOutput

class Client(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.showBase = ShowBase()
        self.accept("escape", self.sendMsgDisconnectReq)
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.Connection = self.cManager.openTCPClientConnection(SERVER_IP, SERVER_PORT, 1)
        self.cReader.addConnection(self.Connection)
        self.showBase.taskMgr.add(self.readTask, "serverReaderPollTask", -39)

        #self.gameOutput = GameOutput(self.showBase)

        def connect():
            self.name = nameEntry.get()
            if self.name != "":
                self.sendMsgAuth()
                loginButton["text"] = "Start!"
                loginButton["command"] = self.sendCompleteSetup
        loginButton = DirectButton(
            text = "connect to server",
            scale = 0.1,
            command = connect,
            frameSize = (-4.5, 4.5, -2, 2.5))

        def setText(textEntered):
	        nameEntry.setText(textEntered)
        def clearText():
	        nameEntry.enterText('')
        nameEntry = DirectEntry(
            scale = 0.1,
            command = setText,
            focusInCommand = clearText,
            pos = (-0.5, 0, -0.5),
            numLines = 1,
            focus = 1,
            relief = DGG.SUNKEN)

    ######################################################################################

    def readTask(self, task):
        while 1:
            (datagram, data, msgID) = self.nonBlockingRead(self.cReader) 
            if msgID is MSG_NONE:
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
                 msgID = MSG_NONE
        else:
            datagram = None
            data = None
            msgID = MSG_NONE
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
        pkg.addUint16(CL_MSG_AUTH)
        pkg.addString(self.name)
        self.send(pkg)

    ######################################################################################

    def msgAuthResponse(self, msgID, data): 
        pkg = PyDatagram()
        pkg.addUint16(CL_MSG_CHAT)
        pkg.addString("client is calling in and is glad to be here")
        self.send(pkg)

    ######################################################################################

    def sendMsgDisconnectReq(self): 
        pkg = PyDatagram() 
        pkg.addUint16(CL_MSG_DISCONNECT_REQ) 
        self.send(pkg) 

    ######################################################################################

    def msgChat(self, msgID, data):
        print data.getString() 

    ######################################################################################

    def msgDisconnectAck(self, msgID, data):  
        self.cManager.closeConnection(self.Connection)  
        sys.exit() 

    ######################################################################################

    def sendCompleteSetup(self):
        pkg = PyDatagram()
        pkg.addUint16(CL_MSG_COMPLETE_SETUP)
        self.send(pkg)

    def sendMovementCommand(self, movement, state):
        pkg = PyDatagram()
        pkg.addUint16(CL_MSG_MOVEMENT_COMMAND)
        pkg.addUint8(movement)
        pkg.addUint8(state)
        self.send(pkg)

    def sendChargeCommand(self, state):
        pkg = PyDatagram()
        pkg.addUint16(CL_MSG_CHARGE_COMMAND)
        pkg.addUint8(state)
        self.send(pkg)

    def sendJumpCommand(self, state):
        pkg = PyDatagram()
        pkg.addUint16(CL_MSG_JUMP_COMMAND)
        pkg.addUint8(state)
        self.send(pkg)

    ######################################################################################

    def send(self, pkg):
        self.cWriter.send(pkg, self.Connection) 

    ######################################################################################

    def handleStartGame(self, msgID, data):
        self.accept("w", self.sendMovementCommand, [PLAYER_MOVEMENT_UP, 1])
        self.accept("a", self.sendMovementCommand, [PLAYER_MOVEMENT_LEFT, 1])
        self.accept("s", self.sendMovementCommand, [PLAYER_MOVEMENT_DOWN, 1])
        self.accept("d", self.sendMovementCommand, [PLAYER_MOVEMENT_RIGHT, 1])
        self.accept("c", self.sendChargeCommand, [1]);
        self.accept("v", self.sendJumpCommand, [1]);
        self.accept("w-up", self.sendMovementCommand, [PLAYER_MOVEMENT_UP, 0])
        self.accept("a-up", self.sendMovementCommand, [PLAYER_MOVEMENT_LEFT, 0])
        self.accept("s-up", self.sendMovementCommand, [PLAYER_MOVEMENT_DOWN, 0])
        self.accept("d-up", self.sendMovementCommand, [PLAYER_MOVEMENT_RIGHT, 0])
        self.accept("c-up", self.sendChargeCommand, [0]);
        self.accept("v-up", self.sendJumpCommand, [0]);
        
        setup = []
        numberOfPlayers = data.getUint16()
        for i in range(0, numberOfPlayers):
            setup.append([data.getString(), Point3(data.getFloat32(), data.getFloat32(), data.getFloat32())])
        #self.gameOutput.start(self.name, setup)

    def handleUpdatePositions(self, msgID, data):
        updates = []
        numberOfPlayers = data.getUint16()
        print "Received %d position updates from server." % numberOfPlayers
        for i in range(0, numberOfPlayers):
            updates.append([
                data.getString(),
                Point3(data.getFloat32(), data.getFloat32(), data.getFloat32()),
                Point3(data.getFloat32(), data.getFloat32(), data.getFloat32())])
        #self.gameOutput.setPlayerPositions(updates)
        for update in updates:
            print "%s: (%f / %f / %f)" % (update[0], update[1][0], update[1][1], update[1][2])

    def handleUpdateStates(self, msgID, data):
        updates = []
        numberOfPlayers = data.getUint16()
        print "Received %d state updates from server." % numberOfPlayers
        for i in range(0, numberOfPlayers):
            updates.append({
                "player" : data.getString(),
                "status" : data.getUint8(),
                "health" : data.getFloat32(),
                "charge" : data.getUint8(),
                "jump" : data.getUint8()})
        #self.gameOutput.setPlayerStates(updates)
        for update in updates:
            print "%s: %d, %.2f, %d, %d" % (update["player"], update["status"], update["health"], update["charge"], update["jump"])

    ######################################################################################

    def quit(self): 
        self.cManager.closeConnection(self.Connection) 
        sys.exit() 

client = Client() 

Handlers = { 
    SV_MSG_AUTH_RESPONSE     : client.msgAuthResponse, 
    SV_MSG_CHAT              : client.msgChat, 
    SV_MSG_DISCONNECT_ACK    : client.msgDisconnectAck,
    SV_MSG_START_GAME        : client.handleStartGame,
    SV_MSG_UPDATE_POSITIONS  : client.handleUpdatePositions,
    SV_MSG_UPDATE_STATES     : client.handleUpdateStates
    } 

run()