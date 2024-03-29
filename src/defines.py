##########################################################################################
# client/server pairing messages #########################################################
##########################################################################################

MSG_NONE                = 0 
CL_MSG_AUTH             = 1 
SV_MSG_AUTH_RESPONSE    = 2 
CL_MSG_CHAT             = 3 
SV_MSG_CHAT             = 4 
CL_MSG_DISCONNECT_REQ   = 5 
SV_MSG_DISCONNECT_ACK   = 6

##########################################################################################
# server messages ########################################################################
##########################################################################################

SV_MSG_START_GAME       = 10
SV_MSG_UPDATE_POSITIONS = 11
SV_MSG_UPDATE_STATES    = 12

##########################################################################################
# client messages ########################################################################
##########################################################################################

CL_MSG_COMPLETE_SETUP   = 20

CL_MSG_MOVEMENT_COMMAND = 50
CL_MSG_CHARGE_COMMAND   = 51
CL_MSG_JUMP_COMMAND     = 52

##########################################################################################
# player states ##########################################################################
##########################################################################################

PLAYER_MOVEMENT_RIGHT   = 1
PLAYER_MOVEMENT_LEFT    = 2
PLAYER_MOVEMENT_UP      = 3
PLAYER_MOVEMENT_DOWN    = 4

PLAYER_STATUS_DEAD = 0
PLAYER_STATUS_NORMAL = 1
PLAYER_STATUS_MOVING = 2
PLAYER_STATUS_JUMPING = 3
PLAYER_STATUS_CHARGING = 4
PLAYER_STATUS_FALLING = 5

PLAYER_CHARGE_NONE = 0
PLAYER_CHARGE_GATHER = 1
PLAYER_CHARGE_UNLEASH = 2
PLAYER_CHARGE_HIT = 3
PLAYER_CHARGE_MISS = 4

PLAYER_JUMP_NONE = 0
PLAYER_JUMP_GATHER = 1
PLAYER_JUMP_UNLEASH = 2
PLAYER_JUMP_FINISH = 3

##########################################################################################
# positions ##############################################################################
##########################################################################################
POSITION_TOP_LEFT = 1
POSITION_TOP_RIGHT = 2
POSITION_BOTTOM_LEFT = 3
POSITION_BOTTOM_RIGHT = 4
