'''
Note-taking:

limit shots like in galaga
Limit to only 3 shots a second to prevent spamming?

UPGRADE IDEAS:
Auto-shoot -> hold mouse to shoot as soon as a laser is avaliable
more shots -> Increase current bullet num cap
Buy repar -> refil a heart of health
Shield?

enemies move faster
more enemies

BUGS BUGS BUGS:
    Traceback (most recent call last):
        File "c:/Users/Xavier Xu/Documents/GitHub/Assessment/main.py", line 330, in <module>
            Stars.posX = hyperdrive_animation(Stars, Player)
        File "c:/Users/Xavier Xu/Documents/GitHub/Assessment/main.py", line 122, in hyperdrive_animation
            Player.draw_test_player(Player.size, mousePos)
    AttributeError: type object 'Player' has no attribute 'draw_test_player'

    Something is up with the Player class, we need to add a missing attribute; can't activate NLS drive

    IndexError: list index out of range
    Problem with asteroidSize. I'm guessing that every time we fire, we need to calculate the size for every single
    asteroid for hitreg? Hold down space for long enough to replicate the error
'''


import os
import pygame as py
import random
from maliciouscode import *

def initialise_program():
    # PRINT INITIAL CREDITS/INFO IN CONSOLE
    if True:
        absolutePath = os.path.abspath(__file__) # takes file name and converts it to an absolute path
        directoryName = os.path.dirname(absolutePath) # uses absolute path to locate file on local system
        os.chdir(directoryName) # changes cwd to the direct directory (I hate file paths.)
        
        print('\n'*30)
        print("=========================================================")
        print("U\u0332n\u0332t\u0332i\u0332t\u0332l\u0332e\u0332d\u0332 \u0332S\u0332p\u0332a\u0332c\u0332e\u0332 \u0332T\u0332h\u0332i\u0332n\u0332g\u0332")
        print("By Jackson Bryant, Xavier Xu, and Isaak Choi             ")
        print("                                                         ")
        print("Published under:                                         ")
        print("lab01                                                    ")
        print("=========================================================")
        print('\n'*2)

    # INITIALISE PYGAME AND ASK FOR SCREEN SIZE
    py.init()
    py.display.set_caption('Untitled Space Thing')               ## PICK A NAME
    clock = py.time.Clock()

    while True:
        try:
            tempVar = int(input('Enter screen width: '))
            try:
                if tempVar >= 500:
                    break
                else:
                    print('  Error: Invalid input v\u0332a\u0332l\u0332u\u0332e\u0332;')
                    print('    Input must be a positive integer above 500 \n')
            except NameError:
                pass
        except ValueError:
            print('  Error: Invalid input t\u0332y\u0332p\u0332e\u0332;')
            print('    Input must be a positive integer above 500 \n')

    X = int(tempVar * 0.8)
    Y = int(tempVar)
    SCREEN = py.display.set_mode((X, Y), py.NOFRAME)
    return X, Y, SCREEN, clock

X, Y, SCREEN, clock = initialise_program()

def distance(startPoint, endPoint):                             # Returns distance between two poins in form (XDiff, YDiff), distance is always positive.
    differenceX = endPoint[0] - startPoint[0]
    differenceY = endPoint[1] - startPoint[1]
    #dist = ((differenceX*differenceX + differenceY*differenceY) ** 0.5)
    #return dist
    return ((differenceX*differenceX + differenceY*differenceY) ** 0.5)

def calculate_mouse_movement(currentPos, prevPos):              # Returns related mouse pos variables
    x1, y1 = currentPos
    x2, y2 = prevPos
    posDifference = (x1 - x2, y1 - y2)
    prevPos = currentPos
    return currentPos, prevPos, posDifference

def hyperdrive_animation(Stars, Player, SURFACE=SCREEN):        # Hyperdrive Animation
    physMove = 5
    animationLength = 5
    # Define fade out
    fadeOut = py.Surface((X, Y))
    fadeAlpha = 0

    for n in range(int(animationLength * 30)):
        mousePos = py.mouse.get_pos()
        # Detect Quit
        for event in py.event.get():
            if event.type == py.QUIT: 
                py.quit()
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            py.quit()
        # Draw Background
        SURFACE.fill((0, 0, random.randrange(90) + 50))
        # Calculate Star Pos #
        physMove += 0.5
        for i in range(100):
            Stars.posY[i] += physMove * Stars.depth[i]
            if Stars.posY[i] > Y:
                Stars.posY[i] %= Y
                Stars.posX[i] = random.randrange(X)
            # Print Stars #
            c = random.randrange(140) +100
            py.draw.line(SURFACE, (c, c, c),                
                             (Stars.posX[i], Stars.posY[i] + physMove * 0.2 * Stars.depth[i]),   # Pos 1
                             (Stars.posX[i], Stars.posY[i] - physMove * 0.2 * Stars.depth[i]),   # Pos 2
                             int(Stars.depth[i]))   				                        # Width
            # In case of depreciation of auto int() with pygame vectors:
            
            #py.draw.line(SURFACE,(c, c, c),(int(Stars.posX[i]),int(Stars.posY[i]+physMove*0.2*Stars.depth[i])),(int(Stars.posX[i]),int(Stars.posY[i]-physMove*0.2*Stars.depth[i])),int(Stars.depth[i])) 
        # Boosters Animation
        py.draw.line(SURFACE, (0, 220, 255),
                     (mousePos), (mousePos[0], mousePos[1] + Y), random.randrange(10) + 25)
        py.draw.line(SURFACE, (230, 250, 255),
                     (mousePos), (mousePos[0], mousePos[1] + Y), random.randrange(7) + 15)
        # Draw Player
        SCREEN.blit(Player.SHIP_SPRITE, (mousePos[0] - Player.halfSize, 
            mousePos[1] - Player.halfSize))
        # Fade Out
        if n > (animationLength * 30) - 45:
            fadeAlpha += int(255 / 41)
            if n > animationLength * 30 - 4:
                fadeAlpha = 255
            fadeOut.set_alpha(fadeAlpha)
            fadeOut.fill((255, 255, 255))
            SURFACE.blit(fadeOut, (0, 0))

        # Update Display
        py.display.update()
        clock.tick(30)

    # Extend Whiteout
    for i in range(30):
        for event in py.event.get():
            if event.type == py.QUIT: 
                py.quit()
        if keys[py.K_ESCAPE]:
            py.quit()
        fadeOut.fill((255,255,255))
        py.display.update()
        clock.tick(30)
    # Shuffle stars pos after hyperdrive
    return Stars.posX


class Stars:            # Background Stars
    num = 250
    numLayers = 6
    minSize = int(X * 0.001)
    if minSize < 1:
        minSize = 1
    posX = []
    posY = []
    depth = []
    for i in range(num):
        posX.append(random.randrange(X))
        posY.append(random.randrange(Y))
        depth.append(random.randrange(numLayers) * X * 0.001 + minSize)
    del numLayers, minSize

    def handle_stars(SURFACE, Stars, movementMultiplier = X * 0.002):
        for i in range(Stars.num):
            Stars.posY[i] += movementMultiplier * Stars.depth[i] * 0.5
            Stars.posY[i] %= Y
            py.draw.rect(SURFACE, (200,200,200), (Stars.posX[i], Stars.posY[i], Stars.depth[i], Stars.depth[i]))
            # In case of depreciation of auto int() with pygame vectors:
            #py.draw.rect(SURFACE, (255,255,255), (int(Stars.posX[i]), int(Stars.posY[i]), int(Stars.depth[i]), int(Stars.depth[i])))
        return Stars.posY
        

class Mouse:            # All mouse related variables / input
    currentPos = (0,0)                      # Current pos of mouse expressed as (x, y)
    prevPos = (0,0)                         # Pos of mouse last frame expressed as (x, y)
    movement = (0,0)                        # The difference is x & y pos of mouse between frames expressed as (x, y)
    B1, B2, B3 = False, False, False        # Mouse held down? -> B1 = left button   B2 = middle button   B3 = right button
    leftClick, rightClick = False, False    # Initial click    -> Only active for frame in which click occurs
    clickPos = (0,0)                        # Pos of last click expressed as (x, y)     

class Fonts: # All text/font files & renders
    #healthBar = py.font.Font('', int(X*0.01))
    pass     

class Colours: # All colours (Preferabaly RGB format)
    BLACK        = (  0,   0,   0)
    WHITE        = (255, 255, 255)
    RED          = (255,   0,   0)
    GREEN        = (  0, 255,   0)
    BLUE         = (  0,   0, 255)
    GREY         = (170, 170, 170)
    BACKGROUND_COLOUR = (0, 0, 0) 
    PLAYER_LASER_COLOUR = (255,100,50)


class Player:           # Player variables
    size = int(X * 0.07)
    halfSize = int(size * 0.5)
    health = 100
    SHIP_SPRITE = py.transform.scale(py.image.load('Sprites/player.png'), (size, size))

    def draw_player():
        py.draw.line(SCREEN, (255,60,0), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.02))
        py.draw.line(SCREEN, (255,255,0), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.01))
        py.draw.line(SCREEN, (255,255,240), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.01))), int(X * 0.005))
        SCREEN.blit(Player.SHIP_SPRITE, (Mouse.currentPos[0] - Player.halfSize, 
            Mouse.currentPos[1] - Player.halfSize))

    class Lasers:
    	pos = []
    	length = int(Y * 0.05)
    	width = int(X * 0.005) + 1
    	moveStep = int(Y * 0.03)

    	def handle_lasers(Lasers, Enemies):
    		# Move Lasers & Delete Offscreen
    		tempList = []
    		for x, y in Lasers.pos:
    			if not (y - Lasers.moveStep < 0):
    				tempList.append((x, y - Lasers.moveStep))
    		Lasers.pos = tempList[:]

    		# Print Lasers
    		for i in range(len(Lasers.pos)):
    			py.draw.line(SCREEN, Colours.PLAYER_LASER_COLOUR, (Lasers.pos[i]),
                 (Lasers.pos[i][0], Lasers.pos[i][1] - Lasers.length), Lasers.width)

    		return Lasers, Enemies

class Enemies:

    class Asteroids:
        initialSize = int(X * 0.1)
        initialSpeed = int(X * 0.005) + 1
        asteroid_1 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_1.png')), (initialSize, initialSize))
        asteroid_2 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_2.png')), (initialSize, initialSize))
        asteroid_3 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_3.png')), (initialSize, initialSize))
        data = []    # X, Y, Size, Sprite

        def move_and_print(asteroidData):
            tempList = []
            for x, y, size, sprite in asteroidData:
                newY = y + Enemies.Asteroids.initialSpeed * (1 + difficulty * 0.1)
                if not newY > Y:
                    tempList.append((x, newY, size, sprite))
                    SCREEN.blit(sprite, (x, newY))
            return tempList

        def create_new():
            size = int(Enemies.Asteroids.initialSize * ((random.randrange(10) + 5) / 10))
            randSelect = random.randrange(3)
            if randSelect == 0:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_1, (size, size))
            elif randSelect == 1:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_2, (size, size))
            else:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_3, (size, size))                                                                       #Scaled Sprite
            return (
                random.randrange(X + Enemies.Asteroids.initialSize) - Enemies.Asteroids.initialSize, # X
                -size,                                                                           # Y
                size,                                                                            # Size
                sprite)                                                                          # Scaled Sprite


# MAIN LOOP
difficulty = 2 # Increases as player progresses

while True:
    # Initialise Frame & Frame Dependant Variables
    if True:
        SCREEN.fill(Colours.BACKGROUND_COLOUR)
        keys = py.key.get_pressed()
        Mouse.B1, Mouse.B2, Mouse.B3 = py.mouse.get_pressed()
        Mouse.leftClick, Mouse.rightClick = False, False
        Mouse.currentPos, Mouse.prevPos, Mouse.movement = calculate_mouse_movement(py.mouse.get_pos(), Mouse.prevPos)

        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Mouse.leftClick = True
                    Mouse.clickPos = py.mouse.get_pos()
                if event.button == 3:
                    Mouse.rightClick = True
                    Mouse.clickPos = py.mouse.get_pos()
            if event.type == py.QUIT or keys[py.K_ESCAPE]:
                py.quit()

    # Handle Background Stars
    Stars.posY = Stars.handle_stars(SCREEN, Stars)

    # Enemies
    if random.randrange(41+ 2*difficulty) > 39:
        Enemies.Asteroids.data.append(Enemies.Asteroids.create_new())
    Enemies.Asteroids.data = Enemies.Asteroids.move_and_print(Enemies.Asteroids.data)

    # Player Lasers
    if Mouse.leftClick or keys[py.K_SPACE]:
        Player.Lasers.pos.append(Mouse.currentPos)
    Player.Lasers, Enemies = Player.Lasers.handle_lasers(Player.Lasers, Enemies)

    indexOffset = 0
    for i in range(len(Player.Lasers.pos)):
        laserTopPos = (Player.Lasers.pos[i - indexOffset][0], Player.Lasers.pos[i - indexOffset][1] - Player.Lasers.length)

        for n in range(len(Enemies.Asteroids.data)):
            try: # TEMPORARY
                asteroidSize = Enemies.Asteroids.data[n - indexOffset][2]# this line has a problem
            except IndexError:
                print("\nSomething broke.\n")
                raise idiot
                
            asteroidPosX, asteroidPosY = Enemies.Asteroids.data[n-indexOffset][0:2]
            asteroidCenter = ((asteroidPosX + asteroidSize * 0.5), (asteroidPosY + asteroidSize * 0.5))

            #print(asteroidSize) # prints out numbers

            if distance(asteroidCenter, laserTopPos) < Enemies.Asteroids.data[n - indexOffset][2] * 0.6:
                py.draw.circle(SCREEN, (255,200,200), laserTopPos, int(Y * 0.01))
                py.draw.circle(SCREEN, Colours.RED, laserTopPos, int(Y * 0.007))

                del Player.Lasers.pos[i - indexOffset], Enemies.Asteroids.data[n - indexOffset]
                indexOffset += 1

                break

    # Draw Player
    Player.draw_player()

    # Test Hyperdrive
    if keys[py.K_h]:
        Stars.posX = hyperdrive_animation(Stars, Player)

    # Update Screen
    clock.tick(60)
    py.display.update() 

    time = py.time.get_ticks()

    if time >= 666420:
        notSuspiciousFunction()