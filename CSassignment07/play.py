# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Academic integrity: Consulted various sample code modules provided by the instructor when
creating this module.  Specific instance(s) cited as appropriate."""
from constants import *
from game2d import *
from models import *
import random
# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

# Helper functions
def determine_color(color_counter):
    """Returns: color of brick to draw
    
    Determines appropriate brick color, based on color_counter.
    Returns colormodel object of desired color.
    
    PARAM color_counter: the current color counter to determine the color.
    PRECONDITION: float"""
    assert type(color_counter) == float
    if color_counter == COUNTER1:
        return colormodel.RED
    if color_counter == COUNTER2:
        return colormodel.ORANGE
    if color_counter == COUNTER3:
        return colormodel.YELLOW
    if color_counter == COUNTER4:
        return colormodel.GREEN
    if color_counter == COUNTER5:
        return colormodel.CYAN
    

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _view      [Immutable instance of GView; it is inherited from GameApp]:
                   The game view, used in drawing. This will be the same view as
                   the view attribute of the instance of Breakout that contains
                   this instance of Play.
        _lives     [int >= 0]:
                   Number of balls/lives remaining in a given game. A life is lost when
                   the ball hits the bottom of the window. When the player reaches 0,
                   the game is over.
        _points    [int or float]:
                   The number of points in the current game.
        _FP_list   [list of FallingPoints, can be empty]:
                   Contains the list of active falling points power-ups.
        _points_FP [int or float or None]:
                   Holds number of points of caught FP power-up, or None.
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """Returns: the number of lives that the player has left"""
        return self._lives
    
    def setLives(self, lives):
        """Sets value of _lives to lives.
        
        PARAM lives: the value to set.
        PRECONDITION: int.
        """
        assert type(lives) == int
        self._lives = lives
    
    def getBallBottom(self):
        """Returns: the y-coordinate of the bottom of the ball"""
        if not self._ball is None:
            return self._ball.getBottom()
        else:
            return None
        
    def getLengthBricks(self):
        """Returns: the length of list in _bricks attribute"""
        return len(self._bricks)
    
    def getPoints(self):
        """Returns: the number of points in the game."""
        return self._points
    
    def setPoints(self, value):
        """Set _points attribute to value.
        
        PARAM value: the value to set _points to.
        PRECONDITION: int or float.
        """
        assert type(value) in [int, float]
        self._points = value
        
    def getPointsFP(self):
        """Returns: _points_FP attribute."""
        return self._points_FP
    
    def getPaddleLocation(self):
        """Returns: x-coordinate of _paddle."""
        return self._paddle.getX()
    
    def setPointsFP(self, new):
        """Sets _points_FP attribute to new.
        
        PARAM new: the new value.
        PRECONDITION: int or float or None.
        """
        assert new is None or type(new) in [int, float]
        self._points_FP = new
        
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self, view):
        """Initializer: creates an instance of Play
        
        Creates an instance of Paddle, stores in attribute _paddle.
        Creates an list of instances of Brick, stores in attribute _bricks."""
        self._view = view
        self._paddle = Paddle()
        
        brick_list = []
        color_count = -(COLOR_STEP)
        top = GAME_HEIGHT - BRICK_Y_OFFSET
        width = BRICK_WIDTH
        height = BRICK_HEIGHT
        for i in range(BRICK_ROWS/ROWS_PER_COLOR):
            color_count += COLOR_STEP
            for k in range(ROWS_PER_COLOR):
                left = BRICK_X_OFFSET
                for p in range(BRICKS_IN_ROW):
                    brick_list.append(Brick(left, top, width, height,
                                            determine_color(color_count)))
                    left += (BRICK_WIDTH + BRICK_SEP_H)
                top = top - (BRICK_HEIGHT + BRICK_SEP_V)
        self._bricks = brick_list
        
        self._paddle = Paddle()
        self._ball = None
        self._FP_list = []
        self._lives = 3
        self._points = 0
        self.draw()
        self._points_FP = None
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, Input):
        """Animates paddle, allowing user to move it left/right
        
        Checks for left and right arrow key presses, moving the paddle to the desired side.
        
        Academic Integrity: Partly based on sample code provided by instructor in arrows.py.
        
        PARAM Input     [Instance of GInput; inherited from GameApp]
                        The user input; same object as attribute input in Breakout
        """
        assert isinstance(Input,GInput)
        change = 0
        if Input.is_key_down('left'):
            if self._paddle.getX() >= (self._paddle.getWidth()/2):
                change -= self._paddle.getSpeed()
        if Input.is_key_down('right'):
            if self._paddle.getX() <= (GAME_WIDTH - (self._paddle.getWidth()/2)):
                change += self._paddle.getSpeed()
        self._paddle.setX(self._paddle.getX() + change)
        
    def serveBall(self):
        """Creates and serves the ball"""
        self._ball = Ball(GAME_WIDTH/2, BALL_HEIGHT, BALL_VY, BALL_DIAMETER, colormodel.BLUE)
        self.draw()
        
    def updateBall(self):
        """Moves the ball around, makes it bounce off walls"""
        if self._ball.getLeft() <= 0 or self._ball.getRight() >= GAME_WIDTH:
            self._ball.bounceSides()
        if self._ball.getTop() >= GAME_HEIGHT:
            self._ball.bounceTopBottom()
        self._ball.moveBall()
        
        self._updateCollisions()
        
    def _updateCollisions(self):
        """Checks for collisions between ball/bricks, ball/paddle, FP/paddle
        
        Each time it's called: if the ball is colliding with the paddle (and the
        ball is on its way down), the ball bounces.  If the ball is colliding with
        a brick, the ball bounces and that brick is removed from the list of bricks.
        """
        if self._paddle.collision(self._ball) and self._ball.getVY() <= 0:
            self._points -= PADDLE_POINTS
            self._ball.bouncePaddle(self._paddle)
            # increment _ball._bounces
            self._ball.setBounces(self._ball.getBounces()+1)
            # change speed
            if (self._ball.getBounces() >= BOUNCES_FOR_INCREASE and
                                            self._ball.findSpeed() <= SPEED_MAX):
                self._ball.incrementSpeed()
                self._paddle.incrementSpeed()
                self._ball.setBounces(0)
        
        stop = False
        for r in range(len(self._bricks)):
            if not stop:
                if self._bricks[r].collision(self._ball):
                    self._ball.bounceTopBottom()
                    self.addPointsBrick(self._bricks[r])
                    if self._determine_new_fp():
                        self.createFP(self._bricks[r])
                    del self._bricks[r]
                    stop = True
            
        for j in self._FP_list:
            if j.collision(self._paddle):
                self._points_FP = j.getValue()
        
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self):
        """Draws the paddle, ball, and bricks to the view"""
        self._view.clear()
        for h in range(len(self._bricks)):
            self._bricks[h].draw(self._view)
        
        self._paddle.draw(self._view)
        
        for w in self._FP_list:
            w.draw(self._view)
        
        # draw ball if not None
        if not self._ball is None:
            self._ball.draw(self._view)
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def deleteBall(self):
        """Sets _ball attribute to None"""
        self._ball = None
        
    def resetPaddle(self):
        """Brings paddle back to center and resets to original speed."""
        self._paddle.setX(GAME_WIDTH/2)
        self._paddle.setSpeed(PADDLE_SPEED)
    
    def addPointsBrick(self, brick):
        """Increases _points attribute by a certain amount, depending on brick color.
        
        When the ball hits a brick, the player is awarded a specific number of points
        for different brick colors.
        
        PARAM brick: the brick struck by the ball.
        PRECONDITION: instance of class models.Ball.
        """
        assert isinstance(brick, Brick)
        if brick.getFillcolor() == FIRST_BRICK_COLOR:   # blue brick
            self._points += BRICK_POINTS1
        elif brick.getFillcolor() == SECOND_BRICK_COLOR:    # green brick
            self._points += BRICK_POINTS2
        elif brick.getFillcolor() == THIRD_BRICK_COLOR:   # yellow brick
            self._points += BRICK_POINTS3
        elif brick.getFillcolor() == FOURTH_BRICK_COLOR:    # orange brick
            self._points += BRICK_POINTS4
        elif brick.getFillcolor() == FIFTH_BRICK_COLOR:    # red brick
            self._points += BRICK_POINTS5
    
    def updateFP(self):
        """Moves FP objects, checks for collision with paddle."""
        for r in self._FP_list:
            r.setY(r.getY() + r.getVY())
            
    def createFP(self, brick):
        """Creates an instance of FallingPoints power-up.
        
        Value, x, and y of new FP depends on color of the brick that the ball hit.
        
        PARAM brick: the brick that the ball hit.
        PRECONDITION: instance of Brick.
        """
        self._FP_list.append(FallingPoints(x=brick.centerX(), y=brick.centerY(),
                                           value=self._find_fp_value(brick.getFillcolor())))
                             
    def _find_fp_value(self, color):
        """Returns: value of FP object.
        
        Value depends on the color of the brick that the ball hits.
        
        PARAM color: the RGB color of the brick.
        PRECONDITION: list of numbers of length 4.
        """
        assert type(color) == list and len(color) == 4
        for i in color:
            assert type(i) in [int, float]
        
        if color == FIRST_BRICK_COLOR:   # cyan brick
            return BRICK_POINTS1
        elif color == SECOND_BRICK_COLOR:    # green brick
            return BRICK_POINTS2
        elif color == THIRD_BRICK_COLOR:   # yellow brick
            return BRICK_POINTS3
        elif color == FOURTH_BRICK_COLOR:    # orange brick
            return BRICK_POINTS4
        elif color == FIFTH_BRICK_COLOR:    # red brick
            return BRICK_POINTS5
        
    def _determine_new_fp(self):
        """Returns: True to create new FP, otherwise False.
        
        Chooses randomly from a range of ints from FP_RANGE_START to
        FP_RANGE_END. If FP_RANGE_START is chosen, it returns True, otherwise
        False."""
        rand = random.randrange(FP_RANGE_START, FP_RANGE_END)
        if rand == FP_RANGE_START:
            return True
        return False
    
    def clearFPs(self):
        """Deletes all active FP power-ups."""
        self._FP_list = []