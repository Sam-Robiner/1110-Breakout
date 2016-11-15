# models.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *
import colormodel
import math
# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.

# Helper functions
def is_color(color):
    """Returns: True if color is a valid color constant from colormodel, False otherwise
    
    PARAM color: the color to check
    PRECONDITION: NONE (color can be any value)"""
    if isinstance(color, colormodel.RGB):
        return True
    return False


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _speed:     [int or float]:
                Max horizontal speed of the paddle when moved.
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """Returns: x-coordinate of middle of paddle"""
        return self.x
    
    def setX(self, new_x):
        """Sets value of x attribute of paddle to new_x
        
        PARAM new_x: desired value for x-coordinate of middle of paddle
        PRECONDITION: int or float
        """
        assert type(new_x) in [int, float]
        self.x = new_x
        
    def getWidth(self):
        """Returns: width of paddle"""
        return self.width
    
    def getSpeed(self):
        """Returns: speed of the paddle."""
        return self._speed
    
    def setSpeed(self, new):
        """Sets the value of _speed attribute to new.
        
        PARAM new: the new speed value.
        PRECONDITION: int or float.
        """
        assert type(new) in [int, float]
        self._speed = new
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        """Initializer: creates instance of Paddle
        
        Uses default values to generate an instance of the game paddle."""
        (GRectangle.__init__(self, x=GAME_WIDTH/2, bottom=PADDLE_OFFSET-(PADDLE_HEIGHT/2),
                             width=PADDLE_WIDTH, height=PADDLE_HEIGHT,
                             fillcolor=colormodel.BLACK, linecolor=colormodel.BLACK))
        self._speed = PADDLE_SPEED
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collision(self, ball):
        """Returns: True if ball is touching paddle, False otherwise.
        
        PARAM ball: The ball to check.
        PRECONDITION: instance of class Ball.
        """
        assert isinstance(ball, Ball)
        return (self.contains(ball.getRight(), ball.getBottom()) or
                                    self.contains(ball.getLeft(), ball.getBottom()))
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def incrementSpeed(self):
        """Multiplies the speed of the paddle by constant."""
        self._speed = self._speed * SPEED_INCREMENT
        
    def leftX(self):
        """Returns: x-coordinate of left of paddle."""
        return self.x - self.width/2
    
    def rightX(self):
        """Returns: x-coordinate of right of paddle."""
        return self.x + self.width/2
    
    def topY(self):
        """Returns: y-coordinate of top of paddle."""
        return self.y + self.height/2
    

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFillcolor(self):
        """Returns: fill color of brick."""
        return self.fillcolor
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, left, top, width, height, fillcolor):
        """Initializer: creates instance of Brick
        
        PARAMETERS:
        left        [Number: int or float]:
                    The x-coordinate of the left edge of the brick.
        top         [Number: int or float]:
                    The y-coordinate of the top edge of the brick.
        width       [Number: int or float]:
                    The width of the brick.
        height      [Number: int or float]:
                    The height of the brick.
        fillcolor   [default colormodel object; e.g. colormodel.RED]
                    The default colormodel object representing the brick color
                    in RGB color space.
        """
        assert type(left) in [int, float]
        assert type(top) in [int, float]
        assert type(width) in [int, float]
        assert type(height) in [int, float]
        assert is_color(fillcolor)
        (GRectangle.__init__(self, left=left, top=top, width=width, height=height,
                             fillcolor=fillcolor, linecolor=fillcolor))
    
    # METHOD TO CHECK FOR COLLISION
    def collision(self, ball):
        """Returns: True if ball is touching brick, False otherwise.
        
        PARAM ball: The ball to check.
        PRECONDITION: instance of class Ball.
        """
        assert isinstance(ball, Ball)
        for k in [ball.getLeft(), ball.getRight()]:
            for w in [ball.getTop(), ball.getBottom()]:
                if self.contains(k, w) == True:
                    return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def centerX(self):
        """Returns: x-coordinate of the center of the brick."""
        return self.left + (self.width/2)
    
    def centerY(self):
        """Returns: y-coordinate of the center of the brick."""
        return self.top - (self.height/2)


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        x:        [int or float]:
                  The x-coordinate of the center of the ball.
        y:        [int or float]:
                  The y-coordinate of the center of the ball.
        fillcolor:[RGB object]:
                  The color of the ball.
        linecolor:[RGB object]:
                  The color of the outside of the ball.
        width:    [int or float]:
                  The horizontal diameter of the ball.
        height:   [int or float]:
                  The vertical diameter of the ball.
        _top:     [int or float]:
                  The y-coordinate of the top of the ball.
        _bottom:  [int or float]:
                  The y-coordinate of the bottom of the ball.
        _left:    [int or float]:
                  The x-coordinate of the left-most point on the ball.
        _right:   [int or float]:
                  The x-coordinate of the right-most point on the ball.
        _bounces  [int]:
                  Keeps track of the number of times the ball bounces off the paddle.
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLeft(self):
        """Returns: x-coordinate of left-most point on the ball"""
        return self._left
    
    def getRight(self):
        """Returns: x-coordinate of right-most point on the ball"""
        return self._right
    
    def getTop(self):
        """Returns: y-coordinate of top of the ball"""
        return self._top
    
    def getBottom(self):
        """Returns: y-coordinate of bottom of the ball"""
        return self._bottom
    
    def getVY(self):
        """Returns: vertical velocity (vy) of the ball"""
        return self._vy
    
    def getBounces(self):
        """Returns: the number of bounces off the paddle"""
        return self._bounces
    
    def setBounces(self, new):
        """Set value of _boucnes to new.
        
        PARAM new: the value to assign to _bounces.
        PRECONDITION: int.
        """
        assert type(new) == int
        self._bounces = new

    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self, x, y, vy, diameter, fillcolor):
        """Initializer: creates instance of Ball
        
        Academic integrity: part of initialization copied from assignment instructions.
        
        PARAMETERS:
        x:        [int or float]:
                  The x-coordinate of the center of the ball.
        y:        [int or float]:
                  The y-coordinate of the center of the ball.
        vy:       [int or float]:
                  The vertical velocity of the ball; negative is down.
        diameter: [int or float]:
                  The diameter (length and width) of the ball.
        fillcolor:[RGB color object]:
                  The color of the ball.
        """
        assert type(x) in [int, float]
        assert type(y) in [int, float]
        assert type(vy) in [int, float]
        assert isinstance(fillcolor, colormodel.RGB)
        (GEllipse.__init__(self, x=x, y=y, width = diameter, height=diameter,
                                        fillcolor=fillcolor, linecolor=fillcolor))
        
        self._vy = vy
        # Academic integrity: _vx initialization copied from instructions
        self._vx = random.uniform(0.5,2.0)   # instructions give numbers here, not constants
        self._vx = self._vx * random.choice([-1, 1])
        
        self._top = self.y + BALL_DIAMETER/2
        self._bottom = self.y - BALL_DIAMETER/2
        self._left = self.x - BALL_DIAMETER/2
        self._right = self.x + BALL_DIAMETER/2
        self._bounces = 4
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """Adjusts location of ball based on velocities
        
        Each time the method is called, the ball is moved one step; each velocity
        is added to its respective coordinate."""
        self.x += self._vx
        self.y += self._vy
        self._top = self.y + BALL_DIAMETER/2
        self._bottom = self.y - BALL_DIAMETER/2
        self._left = self.x - BALL_DIAMETER/2
        self._right = self.x +BALL_DIAMETER/2
        
    def bounceTopBottom(self):
        """Reverses vertical velocity when the ball hits the top or bottom of the window"""
        self._vy = -self._vy
        
    def bouncePaddle(self, paddle):
        """Changes direction of ball after it hits the paddle.
        
        PARAM paddle: the paddle that the ball collides with.
        PRECONDITION: instance of class Paddle.
        """
        self._vy = -self._vy
        self._vx = self._vx + (self.x - paddle.getX()) * BOUNCE_ANGLE_SCALE
    
    def bounceSides(self):
        """Reverses horizontal velocity when the ball hits the sides of the window"""
        self._vx = -self._vx
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def incrementSpeed(self):
        """Increases speed of ball by a specific amount."""
        self._vx = self._vx * SPEED_INCREMENT
        self._vy = self._vy * SPEED_INCREMENT
    
    def findSpeed(self):
        """Returns: the linear speed of the ball."""
        return math.sqrt(self._vx ** 2 + self._vy ** 2)
    
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class FallingPoints(GLabel):
    """Instance is a falling points (FP) power-up.
    
    Extends class GLabel because falling points power-ups are labels with additional
    properties, and need to have velocity and collision detection methods.
    
    The attributes of an instance of this class are those inherited from class GLabel.
    In addition, instances will have the following attributes:
    INSTANCE ATTRIBUTES:
        _vy:        [int or float]:
                    The vertical velocity of the power-up.
        _value:     [int]:
                    The number of points that the power-up is worth.
        _bottom:    [int or float]:
                    The y-coordinate of the bottom of the power-up.
        _left:      [int or float]:
                    The x-coordinate of the left side of the power-up.
        _right:     [int or float]:
                    The x-coordinate of the right side of the power-up.
        _collided:  [True or False]:
                    Keeps track of whether the power-up has collided with the paddle.
    """
    
    # GETTERS AND SETTERS
    def getVY(self):
        """Returns: vy attribute of FP object."""
        return self._vy
    
    def getY(self):
        """Returns: y attribute of FP object."""
        return self.y
    
    def setY(self, value):
        """Sets y attribute to value.
        
        PARAM value: the new y-coordinate to set to.
        PRECONDITION: float or int.
        """
        assert type(value) in [int, float]
        self.y = value
    
    def getValue(self):
        """Returns: value of FP power-up."""
        return self._value

    # INITIALIZER
    def __init__(self, x, y, value):
        """Initializer: creates instance of FallingPoints.
        
        PARAMETERS:
        x           [Number: int or float]:
                    The x-coordinate of the center of the power-up.
        y           [Number: int or float]:
                    The y-coordinate of the center of the power-up.
        value       [Number: int or float]:
                    The number of points that the power-up is worth.
        """
        assert type(x) in [int, float]
        assert type(y) in [int, float]
        assert type(value) in [int, float]
        GLabel.__init__(self, text=str(value), x=x, y=y, font_size=FP_FONT_SIZE,
                        width=FP_WIDTH, height=FP_HEIGHT, fillcolor=colormodel.PINK)
        self._vy = -value * FALLING_SPEED_SCALE
        self._value = value
        self._bottom = y - self.height/2
        self._left = x - self.width/2
        self._right = x + self.width/2
        self._collided = False
        
    # METHODS FOR MOVEMENT, COLLISION DETECTION
    def moveFP(self):
        """Moves FP object by incrementing y by vy"""
        self.y += self._vy
    
    def collision(self, paddle):
        """Returns: True if paddle 'catches' FP power-up, False otherwise.
        
        PARAM paddle: The paddle to check.
        PRECONDITION: instance of class paddle.
        """
        assert isinstance(paddle, Paddle)
        if (abs(self.bottomY() - paddle.topY()) <= 5 and
                                    paddle.leftX() <= self.x <= paddle.rightX()):

            if not self._collided:
                self._collided = True
                return True
        return False

    # OTHER METHODS
    def bottomY(self):
        """Returns y-coordinate of bottom of FP power-up."""
        return self.y - self.height/2