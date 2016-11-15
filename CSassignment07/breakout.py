# breakout.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza.

Academic integrity: Consulted various sample code modules provided by the instructor when
creating this module.  Specific instance(s) cited as appropriate."""
from constants import *
from game2d import *
from play import *
# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py


class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]:
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_NEWGAME.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _last_key_press   [True or False]:
                          Keeps track of whether one or more keys pressed in previous frame
        _last_n_press     [True or False]:
                          Keeps track of whether 'n' key was pressed in previous frame.
        _last_lose_life   [True or False]:
                          Keeps track of whether life was lost in previous frame.
        time              [int or None]:
                          When not None, keeps track of how many animation frames have passed.
                          Each animation frame is approximately 1/60 of a second; when
                          time == 60, 1 second has passed.
        _points_mssg      [GLabel, or None if there is no message to display]:
                          display of the current number of points.
        _FP_mssg     [GLabel, or None is there is no message to display]:
                          message that displays when user catches an FP power-up.
    """

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application, instantiates attributes.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        self._state = STATE_INACTIVE
        self._game = None
        self._last_key_press = False
        self._last_n_press = False
        self._last_lose_life = False
        self._mssg = (GLabel(text=START_MSSG, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, font_size=24))
        self.time = None
        self._points_mssg = None
        self._falling_points = []
        self._FP_mssg = None
        
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        STATE_COMPLETED: The application switches to this state when the game is over.
        A message is displayed, depending on whether the player won or lost. In either
        case, the player may begin a new game from this state.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        
        Academic integrity: Consulted sample code from the provided module state.py.
        """
        # increment timer 
        if not self.time == None:
            self.time = self.time + 1
        
        if self._state == STATE_INACTIVE:
            self._inactive()
        if self._state == STATE_NEWGAME:
            self._newgame()        
        if self._state == STATE_COUNTDOWN:
            self._countdown()
        if self._state == STATE_ACTIVE:
            self._active()
        if self._state == STATE_PAUSED:
            self._paused()
        if self._state == STATE_COMPLETED:
            self._completed()
    
    def draw(self):
        """Draws the message objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if not self._mssg is None:
            self._mssg.draw(self.view)
            
        if not self._FP_mssg is None:
            self._FP_mssg.draw(self.view)
            
        if self._state == STATE_ACTIVE and not self._points_mssg is None:
            self._points_mssg.draw(self.view)
    
    # HELPER METHODS FOR THE STATES GO HERE
    # helper for _inactive
    def _new_key_press(self):
        """Returns: True if there is a new key press, False otherwise
        
        If one or more keys are pressed in the current animation frame AND no keys
        were pressed in the previous animation frame, this method recognizes a new key press.
        
        Academic Integrity: Consulted sample code from provided module state.py"""
        # check for new key press
        if self._last_key_press == False and self.input.key_count > 0:
            return True
        else:
            return False
        
        # update _last_key_press
        self._last_key_press = (self.input.key_count > 0)
        
    # helper for _paused    
    def _new_n_press(self):
        """Returns: True if there is a new key press of 'n' key, False otherwise.
        
        If the 'n' key is pressed in the current animation frame AND it was not pressed
        in the previous animation frame, this method recognizes a new 'n' press."""
        # check for new 'n' press
        if self._last_n_press == False and self.input.is_key_down('n'):
            return True
        else:
            return False
        
        # update _last_n_press
        self._last_key_press = self.input.is_key_down('n')
        
    # helper for _lose_life     
    def _life_minus_one(self):
        """Helper method; decreases _lives by one"""
        if self._last_lose_life == False:
            self._game.setLives(self._game.getLives()-1)
            self._last_lose_life == True
      
    # helper for _active
    def _lose_life(self):
        """Checks whether the ball has hit the bottom (missed paddle), provides instructions.
        
        When the user loses a ball/life, the following processes are enacted:
        1. If the player had 3 or 2 lives left, the state changes to STATE_PAUSED, and a
           message is displayed.
        3. If the player had 1 life left, the state changes to STATE_COMPLETE, and
           a different message is displayed.
        """
        if self._game.getBallBottom() <= 0:
            self._game.clearFPs()
            if self._game.getLives() > 1:
                self.view.clear()
                self._state = STATE_PAUSED
                self._life_minus_one()
            else:
                self. view.clear()
                self._state = STATE_COMPLETED
                self._life_minus_one()
                
    # helper for _active
    def _catchFP(self):
        """Provides instructions when user catches FP power-up."""
        new_points = self._game.getPointsFP()
        self._game.setPoints(self._game.getPoints() + new_points)
        self._FP_mssg = (GLabel(text='+ ' + str(new_points),
                                x=self._game.getPaddleLocation(), y=FP_MSSG_Y,
                                                font_size=FP_MSSG_FONT_SIZE))
        self._game.setPointsFP(None)
        self.time = 0
        self._FP_mssg_timer()
    
    def _FP_mssg_timer(self):
        """Deletes the FP message after a certain amount of time has elapsed."""
        if self.time >= FP_MSSG_TIME:
            self._FP_mssg = None
    
    # STATE-DEPENDENT HELPER METHODS
    def _inactive(self):
        """Provides instructions for state STATE_INACTIVE
        
        Code executed once per animation frame in which state is STATE_INACTIVE.
        See spec for update for more information."""
        if self._new_key_press():
            self._state = STATE_NEWGAME
            self._mssg = None
    
    def _newgame(self):
        """Provides instructions for state STATE_NEWGAME
        
        Code executed once per animation frame in which state is STATE_NEWGAME.
        See spec for update for more information."""
        self._view.clear()
        self._game = Play(self._view)
        self._state = STATE_COUNTDOWN
        self.time = 0
        
    def _countdown(self):
        """Provides instructions for state STATE_COUNTDOWN
        
        Code executed once per animation frame in which state is STATE_COUNTDOWN.
        See spec for update for more information."""
        self._game.deleteBall()
        self._game.draw()
        # reset paddle speed
        self._game.updatePaddle(self.input)
        if ZERO_SECS <= self.time < ONE_SEC:
            self._mssg = (GLabel(text='3', x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                                                    font_size=COUNTDOWN_FONT_SIZE))
        if ONE_SEC <= self.time < TWO_SECS:
            self._mssg = (GLabel(text='2', x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                                                    font_size=COUNTDOWN_FONT_SIZE))
        if TWO_SECS <= self.time < THREE_SECS:
            self._mssg = (GLabel(text='1', x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                                                    font_size=COUNTDOWN_FONT_SIZE))
        if self.time >= THREE_SECS:
            self._mssg = None
            self._game.serveBall()
            self._state = STATE_ACTIVE
            self._points_mssg = (GLabel(text='Points: 0', x=POINTS_X, y=POINTS_Y, font_size=24))
    
    def _active(self):
        """Provides instructions for state STATE_ACTIVE
        
        Code executed once per animation frame in which state is STATE_ACTIVE.
        See spec for update for more information."""
        self._game.updatePaddle(self.input)
        self._game.updateBall()
        self._game.updateFP()
        self._lose_life()
        self._new_n_press()
        self._points_mssg.text = str(self._game.getPoints())
        if not self._game.getPointsFP() is None:
            self._catchFP()
        self._FP_mssg_timer()
        # check for victory
        if self._game.getLengthBricks() <= 0:
            self._state = STATE_COMPLETED
        
        self.draw()
        self._game.draw()
    
    def _paused(self):
        """Provides instructions for state STATE_PAUSED
        
        Code executed once per animation frame in which state is STATE_PAUSED.
        See spec for update for more information."""
        self.view.clear()
        if self._game.getLives() == 2:
            self._mssg = (GLabel(text=TWO_LIFE_MSSG, x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                                                                    font_size=20))
        elif self._game.getLives() == 1:
            self._mssg = (GLabel(text=ONE_LIFE_MSSG, x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
            
                                                                    font_size=20))
        if self._new_n_press():
            self._state = STATE_COUNTDOWN
            self._mssg = None
            self._game.resetPaddle()
            self.time = 0
    
    def _completed(self):
        """Provides instructions for state STATE_COMPLETED
        
        Code executed once per animation frame in which state is STATE_COMPLETED.
        See spec for update for more information."""
        if self._game.getLives() == 0:   # loss
            self.view.clear()
            self._mssg = (GLabel(text=LOSS_MSSG, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, font_size=16))
        else:  # win
            self.view.clear()
            self._mssg = (GLabel(text='You won! (' + str(self._game.getPoints()) + ' Points)' +
                                 WIN_MSSG, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, font_size=16))
           
        if self._new_n_press():
            self._state = STATE_NEWGAME
            self._mssg = None  