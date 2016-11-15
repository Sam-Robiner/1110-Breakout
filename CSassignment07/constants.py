# constants.py
# Walker M. White (wmw2)
# November 12, 2014
"""Constants for Breakout

This module global constants for the game Breakout.  These constants 
need to be used in the model, the view, and the controller. As these
are spread across multiple modules, we separate the constants into
their own module. This allows all modules to access them."""
import colormodel
import sys

######### WINDOW CONSTANTS (all coordinates are in pixels) #########

#: the width of the game display 
GAME_WIDTH  = 480
#: the height of the game display
GAME_HEIGHT = 620

######### PADDLE CONSTANTS #########
#: the width of the paddle
PADDLE_WIDTH  = 64
#: the height of the paddle
PADDLE_HEIGHT = 11
#: the distance of the (bottom of the) paddle from the bottom
PADDLE_OFFSET = 30

######### BRICK CONSTANTS #########
#: the horizontal separation between bricks
BRICK_SEP_H    = 5
#: the vertical separation between bricks
BRICK_SEP_V    = 4
#: the height of a brick
BRICK_HEIGHT   = 9
#: the offset of the top brick row from the top
BRICK_Y_OFFSET = 70
#: the number of bricks per row
BRICKS_IN_ROW  = 10
#: the number of rows of bricks, in range 1..10.
BRICK_ROWS     = 10
#: the width of a brick
BRICK_WIDTH    = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H

######### BALL CONSTANTS #########
#: the diameter of the ball in pixels
BALL_DIAMETER = 18
#: the starting y-coordinate of the ball
BALL_HEIGHT = GAME_HEIGHT / 2 + 100

######### GAME CONSTANTS #########
#: the number of attempts in a game
NUMBER_TURNS = 3
#: state before the game has started
STATE_INACTIVE  = 0
#: state when we are initializing a new game
STATE_NEWGAME   = 1
#: state when we are counting down to the ball serve
STATE_COUNTDOWN = 2
#: state when we are waiting for user to click the mouse
STATE_PAUSED    = 3
#: state when the ball is in play and being animated
STATE_ACTIVE    = 4
#: state when the game is over
STATE_COMPLETED  = 5

######### COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF BRICKS IN ROW #########
"""sys.argv is a list of the command line arguments when you run
python. These arguments are everything after the work python. So
if you start the game typing

    python breakout.py 3 4
    
Python puts ['breakout.py', '3', '4'] into sys.argv. Below, we 
take advantage of this fact to change the constants BRICKS_IN_ROW
and BRICK_ROWS"""

try:
   if (not sys.argv is None and len(sys.argv) == 3):
        bs_in_row  = int(sys.argv[1])
        brick_rows = int(sys.argv[2])
        if (bs_in_row > 0 and brick_rows > 0):
            # ALTER THE CONSTANTS
            BRICKS_IN_ROW  = bs_in_row
            BRICK_ROWS     = brick_rows
            BRICK_WIDTH    = GAME_WIDTH / BRICKS_IN_ROW - BRICK_SEP_H
except: # Leave the contants alone
    pass

######### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY #########
######### OTHER BALL CONSTANTS #########
#: initial vertical velocity of the ball
BALL_VY = -4.2
#: scale factor for adjustment of ball._vx after bounce on paddle
BOUNCE_ANGLE_SCALE = 0.08
#: amount to multiply ball horizonal and vertiacl speed by every time speed increases
SPEED_INCREMENT = 1.2
#: number of bounces before the ball speed is increased
BOUNCES_FOR_INCREASE = 5
#: max total speed of ball
SPEED_MAX = 7.4

######### OTHER PADDLE CONSTANTS #########
#: initial velocity of paddle when moved horizontally
PADDLE_SPEED = 4.3

######### OTHER BRICK CONSTANTS #########
#: offset of the left brick column from the left, and the right brick column from the right
BRICK_X_OFFSET = (GAME_WIDTH - (10*BRICK_WIDTH) - (9*BRICK_SEP_H))/2
#: number of rows of bricks of each color
ROWS_PER_COLOR = 2
#: number of different brick colors
NUM_COLORS = 5
#: list representing the color of the first (bottom) two rows of bricks
FIRST_BRICK_COLOR = [0.0, 1.0, 1.0, 1.0]
#: list representing the color of the second two rows of bricks
SECOND_BRICK_COLOR = [0.0, 1.0, 0.0, 1.0]
#: list representing the color of the third two rows of bricks
THIRD_BRICK_COLOR = [1.0, 1.0, 0.0, 1.0]
#: list representing the color of the fourth two rows of bricks
FOURTH_BRICK_COLOR = [1.0, 0.7843137254901961, 0.0, 1.0]
#: list representing the color of the fifth (top) two rows of bricks
FIFTH_BRICK_COLOR = [1.0, 0.0, 0.0, 1.0]

######### POWER-UP CONSTANTS #########
#: Scale factor for downward velocity of falling points power-up.
FALLING_SPEED_SCALE = 0.05
#: Width of falling points power-up.
FP_WIDTH = BRICK_WIDTH / 2
#: Height of falling points power-up.
FP_HEIGHT = BRICK_HEIGHT / 2
#: Font size used for falling points power-up.
FP_FONT_SIZE = 12
#: Start of range used to determine whether to create a new FP. See spec of play.determine_new_fp.
FP_RANGE_START = 1
#: End of range used to determine whether to create a new FP. See spec of play.determine_new_fp.
FP_RANGE_END = 5

######### MESSAGE CONSTANTS #########
#: message displayed before the start of the first game
START_MSSG = 'Welcome to Breakout!\nUse the arrow keys to move.\nPress any key to start.'
#: message displayed when player has two lives remaining
TWO_LIFE_MSSG = "Lives Remaining: 2\nPress 'n' for a new ball."
#: message displayed when player has one life remaining
ONE_LIFE_MSSG = "Lives Remaining: 1 (Don't mess up)\nPress 'n' for a new ball."
#: message displayed after player wins, minus the first line
WIN_MSSG = ("\n\n\"When I have reached a summit, I leave it with great reluctance,\n" +
                        "unless it is to reach for another, higher one.\" -- Gustav " +
                     "Mahler\n\nIf you dare to reach higher, press 'n' to play again.")
#: message displayed after player loses
LOSS_MSSG = ("\"Endurance is one of the most difficult disciplines, but it is\nto the " +
                                   "one who endures that the final victory " +
                                  "comes.\" -- Buddha\n\nPress 'n' to play again.")
#: x-coordinate of points message
POINTS_X = GAME_WIDTH - 30
#: y-coordinate of points message
POINTS_Y = GAME_HEIGHT - 12
#: Height of the FP message.
FP_MSSG_HEIGHT = PADDLE_HEIGHT
#: y-coordinate of the FP message.
FP_MSSG_Y = PADDLE_OFFSET + PADDLE_HEIGHT + FP_MSSG_HEIGHT/2
#: Font size of FP message.
FP_MSSG_FONT_SIZE = 12
#: Amount of time (in animation frames) that the FP message is displayed for.
FP_MSSG_TIME = 40
#: Font size of countdown message.
COUNTDOWN_FONT_SIZE = 42

######### OTHER CONSTANTS #########
#: amount to change color counter each row
COLOR_STEP = 1.0
#: value of color counter corresponding to the first color
COUNTER1 = 0.0
#: value of color counter corresponding to the second color
COUNTER2 = 1.0
#: value of color counter corresponding to the third color
COUNTER3 = 2.0
#: value of color counter corresponding to the fourth color
COUNTER4 = 3.0
#: value of color counter corresponding to the fifth color
COUNTER5 = 4.0
#: number of animation frames in 0 seconds
ZERO_SECS = 0
#: number of animation frames in 1 second
ONE_SEC = 60
#: number of animation frames in 2 seconds
TWO_SECS = 120
#: number of animation frames in 3 seconds
THREE_SECS = 180
#: Number of points the player loses each time the ball hits the paddle
PADDLE_POINTS = 6
#: Number of points the player gets when the ball hits a brick in the first two rows
BRICK_POINTS1 = 25
#: Number of points the player gets when the ball hits a brick in the second two rows
BRICK_POINTS2 = 50
#: Number of points the player gets when the ball hits a brick in the third two rows
BRICK_POINTS3 = 75
#: Number of points the player gets when the ball hits a brick in the fourth two rows
BRICK_POINTS4 = 100
#: Number of points the player gets when the ball hits a brick in the fifth two rows
BRICK_POINTS5 = 150