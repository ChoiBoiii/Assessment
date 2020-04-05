'''
HOW TO COPY THE VALUES OF A CLASS AT A GIVEN TIME, NOT BUILD A REFERENCE TO THE CLASS?

NOTES:
- Add highscores page 
- Add upgrades shop
- Add level incrementation -> increase difficulty, access shop
- ALL DOCUENTATION; DFD, IPO's, GANTT, LOGBOOKS, PROJECT SCOPE THINGO, ETC 

UPGRADE IDEAS:
Auto-shoot -> hold mouse to shoot as soon as a laser is avaliable   -YES   BUY FOR 2000 POINTS 
more shots -> Increase current bullet num cap                       -YES   BUY FOR 3000 POINTS 
buy bullets -> add ammo counter, player has to buy more             -YES   BUY FOR 2 POINTS EACH, in lots of 50 (50 for 100 points)
Buy repair -> refil a heart of health   - NO ONLY ONE LIFE
Shield? -> Nah shield's for noobs                                   -YES   BUY FOR 5000 POINTS (only one avaliable?)
BOMBS -> Destroy everything on screen                               -YES   BUY FOR 500 POINTS

BUGS BUGS BUGS:
    Could this be!? No bugs?? Ha you wish.
    After a while the gun just stops working. Idk if I'm out of ammo or what
    When exiting hyperspace, there's a chance you'll spawn inside an asteroid and PERISH WITH IMMEDIATE EFFECT

    Also when you quit the game, the game actually crashes lmao

'''

import os
import pygame as py
import random
import copy
# from maliciouscode import *

def user_screen_size_input(): # Creates game screen based on user input
    #-> Not needed as screen is automatically set based on the size of their monitor
    while True:
        try:
            tempVar = int(input('Enter screen height: '))
            try:
                if tempVar >= 500:
                    print("Initializing...")
                    break
                else:
                    print('  Error: Invalid input v\u0332a\u0332l\u0332u\u0332e\u0332;')
                    print('    Input must be a positive integer above 500 \n')
            except NameError:
                pass
        except ValueError:
            print('  Error: Invalid input t\u0332y\u0332p\u0332e\u0332;')
            print('    Input must be a positive integer above 500 \n')
    screenDimensions = (int(tempVar*0.8), int(tempVar))
    return screenDimensions

def system_screen_size_input(): # Creates game screen based on monitor size
    reduceFromMaxSize = 0.8
    monitorWidth = py.display.Info().current_w
    monitorHeight = py.display.Info().current_h

    if monitorHeight*0.8 < monitorWidth:
        X = int(monitorHeight*0.8 *reduceFromMaxSize)
        Y = int(monitorHeight *reduceFromMaxSize)
    elif monitorWidth*1.25 < monitorHeight:
        X = int(monitorWidth *reduceFromMaxSize)
        Y = int(monitorWidth*1.25 *reduceFromMaxSize)
    else: # Backup in case both width and height tests fail, get user to input
        X, Y = user_screen_size_input()
    return X, Y

def initialise_program(): # Set up display and pygame
    absolutePath = os.path.abspath(__file__) # takes file name and converts it to an absolute path
    directoryName = os.path.dirname(absolutePath) # uses absolute path to locate file on local system
    os.chdir(directoryName) # changes cwd to the direct directory (I hate file paths.)

    # PRINT INITIAL CREDITS/INFO IN CONSOLE
    
    print('\n'*30)
    print("=========================================================")
    print("U\u0332n\u0332t\u0332i\u0332t\u0332l\u0332e\u0332d\u0332 \u0332S\u0332p\u0332a\u0332c\u0332e\u0332 \u0332T\u0332h\u0332i\u0332n\u0332g\u0332")
    print("By Jackson Bryant, Xavier Xu, and Isaak Choi             ")
    print("                                                         ")
    print("Published under:                                         ")
    print("lab01                                                    ")
    print("=========================================================")
    print("")
    print("Some aspects of this game require timing between music and frames,")
    print("Please exit any applications in the background so that it runs smoothly")
    print("Best experienced with headphones")

    # GAME INSTRUCTIONS
    print("""
    Enemies                 | 50 points
    Asteroids               | 10 points
    Somehow miss everything | -5 points

    Move   | [Mouse]
    Shoot  | [Left Click]
    Quit   | [ESCAPE]
    Bomb   | [SPACE]

    You only have one life so
    DON'T GET HIT!
    """)

    print("Initializing... \n")

    # INITIALISE PYGAME AND GET SCREEN SIZE
    py.init()
    py.display.set_caption('Untitled Space Thing')    
    clock = py.time.Clock()
    X, Y = system_screen_size_input()

    # Initialise display
    SCREEN = py.display.set_mode((X, Y), py.NOFRAME)
    return X, Y, SCREEN, clock

X, Y, SCREEN, clock = initialise_program()
del initialise_program, system_screen_size_input, user_screen_size_input # No longer needed -> Memmory management

def distance(startPoint, endPoint): # Returns distance between two poins in form (XDiff, YDiff), distance is always positive.
    differenceX = endPoint[0] - startPoint[0]
    differenceY = endPoint[1] - startPoint[1]
    #dist = ((differenceX*differenceX + differenceY*differenceY) ** 0.5)
    #return dist
    return ((differenceX*differenceX + differenceY*differenceY) ** 0.5)

def colour_loop_RGB(colourPoints, length, currentPoint):
    sectionLen = int(length / len(colourPoints))
    i = int(currentPoint/sectionLen) 
    fadeFrom = colourPoints[i%len(colourPoints)]
    fadeTo = colourPoints[(i+1)%len(colourPoints)]
    differenceStep1 = (fadeTo[0]-fadeFrom[0])/sectionLen
    differenceStep2 = (fadeTo[1]-fadeFrom[1])/sectionLen
    differenceStep3 = (fadeTo[2]-fadeFrom[2])/sectionLen
    n = currentPoint%sectionLen
    return (int(fadeFrom[0] + differenceStep1*n), int(fadeFrom[1] + differenceStep2*n), int(fadeFrom[2] + differenceStep3*n)) # produce ordered colour-points via an RGB gradient generated from given colour-points

def handle_highscores(): # Pull scores from file, add player score, sort, return top 10 + re-write to file
    ## READ FILE ##
    highscores = []
    for line in open(os.path.join('highscores.txt')):
        highscores.append(int(line.strip()))
    # Add Player Score #
    highscores.append(Player.score)
    # Sort Scores In Order #
    highscores = sorted(highscores)
    highscores = highscores[::-1]
    highscoresLen = len(highscores)
    # Remove Scores Below Top 10 #
    if highscoresLen > 10:
        highscores = highscores[:10]
        highscoresLen = 10

    ## HANDLE SAVING OF SCORES TO HIGHSCORES FILE ##
    with open(os.path.join("highscores.txt"), 'w') as file:
        for i, score in enumerate(highscores):
            if i < highscoresLen:
                file.write(f'{score}\n')
            else:
                file.write(f'{score}')

    ## RETURN TOP 10 ##
    return highscores, highscoresLen

def intro_screen(playerShip): # Intoduction to basic game overview + controls 
    global firstRun

    ## RGB COLOUR LOOP VARIABLES ##
    currentPointRGB = 0
    loopLengthRGB = 250
    colourPointsRGB = [(255,0,0), (255,0,255), (0,0,255), (0,255,255), (0,255,0), (255,255,0)]

    ## INITIAL VARIABLES ##
    font = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.03))
    titleFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.045))
    titleColour = colour_loop_RGB(colourPointsRGB, loopLengthRGB, currentPointRGB)
    textShade = 255
    textTicks = 0
    textShadeLimit = (50,255)
    shipCenter = (int(X*0.5), int(Y*0.7))
    mainTextColour = (200,255,200)
    ticks = 0

    ## SET UP MAIN TEXT ##
    text1 = font.render("Click the ship to start!", True, (textShade,textShade,textShade), (0,0,0))
    textbox1 = text1.get_rect()
    textbox1.center = (int(X*0.5), int(Y*0.6))

    text2 = font.render("Enemies     | 50 Points", True, mainTextColour, (0,0,0))
    textbox2 = text2.get_rect()
    textbox2.center = (int(X*0.5), int(Y*0.4))

    text3 = font.render("Asteroids   | 10 Points", True, mainTextColour, (0,0,0))
    textbox3 = text3.get_rect()
    textbox3.center = (int(X*0.5), int(Y*0.45))

    text4 = font.render("Miss        | -5 Points", True, mainTextColour, (0,0,0))
    textbox4 = text4.get_rect()
    textbox4.center = (int(X*0.5), int(Y*0.5))

    text5 = font.render("Move with [mouse]", True, mainTextColour, (0,0,0))
    textbox5 = text5.get_rect()
    textbox5.center = (int(X*0.5), int(Y*0.25))

    text6 = font.render("Shoot with [left click]", True, mainTextColour, (0,0,0))
    textbox6 = text6.get_rect()
    textbox6.center = (int(X*0.5), int(Y*0.3))

    text7 = font.render("You only have one life, so", True, mainTextColour, (0,0,0))
    textbox7 = text7.get_rect()
    textbox7.center = (int(X*0.5), int(Y*0.85))

    text8 = font.render("DON'T GET HIT", True, (200,0,0), (0,0,0))
    textbox8 = text8.get_rect()
    textbox8.center = (int(X*0.5), int(Y*0.9))

    titleText = titleFont.render("Untitled Space Thing", True, titleColour, (0,0,0))
    titleTextbox = titleText.get_rect()
    titleTextbox.center = (int(X*0.5), int(Y*0.1))
    #######################

    ## START MUSIC ##
    if firstRun:
        py.mixer.music.stop()
        py.mixer.music.load(os.path.join('Sounds', 'music', 'main_page_music.wav'))
        py.mixer.music.play(-1)
        firstRun = False

    ## MAIN SCREEN LOOP ##
    while True:
        ## INTER-FRAME HANDLING ##
        SCREEN.fill(Colours.BACKGROUND_COLOUR)
        keys = py.key.get_pressed()
        Mouse.leftClick, Mouse.rightClick = False, False
        Mouse.currentPos, Mouse.prevPos, Mouse.movement = Mouse.calculate_movement(py.mouse.get_pos(), Mouse.prevPos)
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Mouse.leftClick = True
                if event.button == 3:
                    Mouse.rightClick = True
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()
        if Mouse.leftClick:
            if int(shipCenter[0]-Player.halfSize*1.5) < Mouse.currentPos[0] < int(shipCenter[0]-Player.halfSize*1.5 + Player.size*1.5):
                if int(shipCenter[1]-Player.halfSize*1.5) < Mouse.currentPos[1] < int(shipCenter[1]-Player.halfSize*1.5 + Player.size*1.8):
                    break

        ## DYNAMIC TEXT ##
        if textTicks %2 == 0:
            textShade -= 4
            if textShade < textShadeLimit[0]:
                textShade = textShadeLimit[0]
                textTicks += 1
        if textTicks %2 == 1:
            textShade += 4
            if textShade > textShadeLimit[1]:
                textShade = textShadeLimit[1]
                textTicks += 1
        text1 = font.render("Click the ship to start!", True, (textShade,textShade,textShade), (0,0,0))

        currentPointRGB = ticks%loopLengthRGB
        titleText = titleFont.render("Untitled Space Thing", True, colour_loop_RGB(colourPointsRGB, loopLengthRGB, currentPointRGB), (0,0,0))

        ## PRINT TEXT ##
        SCREEN.blit(text1, textbox1)
        SCREEN.blit(text2, textbox2)
        SCREEN.blit(text3, textbox3)
        SCREEN.blit(text4, textbox4)
        SCREEN.blit(text5, textbox5)
        SCREEN.blit(text6, textbox6)
        SCREEN.blit(text7, textbox7)
        SCREEN.blit(text8, textbox8)
        SCREEN.blit(titleText, titleTextbox)

        ## HANDLE STARS ##
        Stars.posY = Stars.handle_stars(SCREEN, Stars, X*0.001)
        
        ## HANDLE PLAYER SHIP
        py.draw.line(SCREEN, (255,60,0), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.02))
        py.draw.line(SCREEN, (255,255,0), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.01))
        py.draw.line(SCREEN, (255,255,240), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.01))), int(X * 0.005))
        SCREEN.blit(playerShip, (shipCenter[0]-Player.halfSize, shipCenter[1]-Player.halfSize))
        py.draw.rect(SCREEN, (textShade,textShade,textShade), 
            (int(shipCenter[0]-Player.halfSize*1.5), int(shipCenter[1]-Player.halfSize*1.5), int(Player.size*1.5), int(Player.size*1.8)), int(X*0.005 +1))

        ## UPDATE SCREEN + FRAME DELAY ##
        py.display.update()
        clock.tick(40)
        ticks += 1

    return Stars.posY 

def intro_hyperdrive_animation(Stars, Player, animationLength=7.3, SURFACE=SCREEN): # Hyperdrive Animation ~but different~
    ## DISABLE MOUSE VISIBILITY ##
    py.mouse.set_visible(0) 
    ## INITIALISE GAME MUSIC ##
    py.mixer.music.stop()
    py.mixer.music.load(os.path.join('Sounds', 'music', 'game_music.wav'))
    py.mixer.music.play(-1)
    ## INTRO VARIABELS ##
    physMove = 0
    fadeOut = py.Surface((X, Y))
    fadeAlpha = 0
    if py.mouse.get_pos() == (0,0):
        mousePos = (int(X*0.5), int(Y*0.7))
    else:
        mousePos = py.mouse.get_pos()
    ## MAIN ANIMATION LOOP ##
    for n in range(int(animationLength * 30)):
        ## INTER FRAME HANDLING ##
        for event in py.event.get():
            if event.type == py.QUIT: 
                py.display.quit()
                py.quit()
            if event.type == py.MOUSEMOTION:
                mousePos = py.mouse.get_pos()
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()
        SURFACE.fill((0, 0, random.randrange(90) + 50))

        ## HANDLE STARS ##
        physMove += 0.2
        for i in range(100):
            Stars.posY[i] += physMove * Stars.depth[i]
            if Stars.posY[i] > Y:
                Stars.posY[i] %= Y
                Stars.posX[i] = random.randrange(X)
            ## IF NEED TO SPEED UP REMOVE COLOUR CHANGING OF STARS BELOW ##
            c = random.randrange(140) +100
            py.draw.line(SURFACE, (c, c, c),                
                             (Stars.posX[i], int(Stars.posY[i] + physMove * 0.2 * Stars.depth[i])), 
                             (Stars.posX[i], int(Stars.posY[i] - physMove * 0.2 * Stars.depth[i])), 
                             int(Stars.depth[i])) 

        ## SHAKE OFFSETS FOR PLAYER SHIP + BOOSTERS ##
        playerOffsetX = (random.randrange(int(X*0.002*(n/20+1)))-int(X*0.005))
        playerOffsetY = (random.randrange(int(X*0.002*(n/20+1)))-int(X*0.005))

        ## BOOSTERS ANIMATION ##
        py.draw.line(SURFACE, (0, 220, 255),
                     (mousePos[0]+playerOffsetX, mousePos[1]+int(X*0.005)+playerOffsetY), 
                     (mousePos[0]+playerOffsetX, mousePos[1] + Y), 
                     random.randrange(int(Y*0.012)) + int(Y*0.028))
        py.draw.line(SURFACE, (230, 250, 255),
                     (mousePos[0]+playerOffsetX, mousePos[1]+int(X*0.005)+playerOffsetY), 
                     (mousePos[0]+playerOffsetX, mousePos[1] + Y), 
                     random.randrange(int(Y*0.009)) + int(Y*0.013))
        
        ## DRAW PLAYER ##
        SCREEN.blit(Player.SHIP_SPRITE, (mousePos[0] - Player.halfSize +playerOffsetX, 
            mousePos[1] - Player.halfSize +playerOffsetY))

        ## FADE OUT ##
        if n > (animationLength * 30) - 45:
            fadeAlpha += int(255 / 41)
            if n > animationLength * 30 - 4:
                fadeAlpha = 255
            fadeOut.set_alpha(fadeAlpha)
            fadeOut.fill((255, 255, 255))
            SURFACE.blit(fadeOut, (0, 0))

        ## UPDATE DISPLAY ##
        py.display.update()
        clock.tick(30)

    ## EXTENDED WHITEOUT ##
    for i in range(30):
        for event in py.event.get():
            if event.type == py.QUIT: 
                py.display.quit()
                py.quit()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()
        fadeOut.fill((255,255,255))
        py.display.update()
        clock.tick(30)

    ## RETURN SHUFFLED STARS POS ##
    py.mixer.Sound.play(Sounds.hyperdriveExit)
    return Stars.posX

def hyperdrive_animation(Stars, Player, animationLength=5, SURFACE=SCREEN): # Hyperdrive Animation
    ## INTRO VARIABELS ##
    physMove = 0
    fadeOut = py.Surface((X, Y))
    fadeAlpha = 0
    if py.mouse.get_pos() == (0,0):
        mousePos = (int(X*0.5), int(Y*0.7))
    else:
        mousePos = py.mouse.get_pos()
    ## MAIN ANIMATION LOOP ##
    for n in range(int(animationLength * 30)):
        ## INTER FRAME HANDLING ##
        for event in py.event.get():
            if event.type == py.QUIT: 
                py.display.quit()
                py.quit()
            if event.type == py.MOUSEMOTION:
                mousePos = py.mouse.get_pos()
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()
        SURFACE.fill((0, 0, random.randrange(90) + 50))

        ## HANDLE STARS ##
        physMove += 0.2
        for i in range(100):
            Stars.posY[i] += physMove * Stars.depth[i]
            if Stars.posY[i] > Y:
                Stars.posY[i] %= Y
                Stars.posX[i] = random.randrange(X)

    ## IF NEED TO SPEED UP REMOVE COLOUR CHANGING OF STARS BELOW ##
            c = random.randrange(140) +100
            py.draw.line(SURFACE, (c, c, c),                
                             (Stars.posX[i], int(Stars.posY[i] + physMove * 0.2 * Stars.depth[i])), 
                             (Stars.posX[i], int(Stars.posY[i] - physMove * 0.2 * Stars.depth[i])), 
                             int(Stars.depth[i])) 

        ## SHAKE OFFSETS FOR PLAYER SHIP + BOOSTERS ##
        playerOffsetX = (random.randrange(int(X*0.002*(n/20+1)))   -int(X*0.005))
        playerOffsetY = (random.randrange(int(X*0.002*(n/20+1)))   -int(X*0.005))

        ## BOOSTERS ANIMATION ##
        py.draw.line(SURFACE, (0, 220, 255),
                     (mousePos[0]+playerOffsetX, mousePos[1]+int(X*0.005)+playerOffsetY), 
                     (mousePos[0]+playerOffsetX, mousePos[1] + Y), 
                     random.randrange(int(Y*0.012)) + int(Y*0.028))
        py.draw.line(SURFACE, (230, 250, 255),
                     (mousePos[0]+playerOffsetX, mousePos[1]+int(X*0.005)+playerOffsetY), 
                     (mousePos[0]+playerOffsetX, mousePos[1] + Y), 
                     random.randrange(int(Y*0.009)) + int(Y*0.013))
        
        ## DRAW PLAYER ##
        SCREEN.blit(Player.SHIP_SPRITE, (mousePos[0] - Player.halfSize +playerOffsetX, 
            mousePos[1] - Player.halfSize +playerOffsetY))

        ## FADE OUT ##
        if n > (animationLength * 30) - 45:
            fadeAlpha += int(255 / 41)
            if n > animationLength * 30 - 4:
                fadeAlpha = 255
            fadeOut.set_alpha(fadeAlpha)
            fadeOut.fill((255, 255, 255))
            SURFACE.blit(fadeOut, (0, 0))

        ## UPDATE DISPLAY ##
        py.display.update()
        clock.tick(30)

    ## PLAY EXIT SFX ##
    py.mixer.Sound.play(Sounds.hyperdriveExit)

    ## RETURN SHUFFLED STARS POS ##
    return Stars.posX

def shop_screen(): # Screen in between levels; gives player option to buy upgrades with points
    ## MAKE MOUSE VISIBLE ##
    py.mouse.set_visible(1)
    ticks = 0

    ## INITIALISE TEXT & BUTTONS ##
    BUTTON_SIZE = (int(X*0.4), int(Y*0.15))

    # Upgrades Title #
    currentPointRGB = 0
    loopLengthRGB = 250
    colourPointsRGB = [(255,0,0), (255,0,255), (0,0,255), (0,255,255), (0,255,0), (255,255,0)]
    upgradesTitleFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.06))
    upgradesTitleText = upgradesTitleFont.render("UPGRADES!", True, colour_loop_RGB(colourPointsRGB, loopLengthRGB, ticks%loopLengthRGB), (0,0,0))
    upgradesTitleTextbox = upgradesTitleText.get_rect()
    upgradesTitleTextbox.center = (int(X*0.5), int(Y*0.1))

    # Buy Ammo Button #
    AMMO_BUTTON_POS = (int(X*0.05), int(X*0.2))
    AMMO_BUTTON_DATA = (AMMO_BUTTON_POS[0], AMMO_BUTTON_POS[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
    AMMO_BUTTON_COLOUR = (100,100,100) # Changed Later

    # Buy Autoshoot Button #
    AUTOSHOOT_BUTTON_POS = (int(X*0.55), int(X*0.2))
    AUTOSHOOT_BUTTON_DATA = (AUTOSHOOT_BUTTON_POS[0], AUTOSHOOT_BUTTON_POS[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
    AUTOSHOOT_BUTTON_COLOUR = (100,100,100) # Changed Later

    # Buy Max Shot Increase Button #
    MAX_SHOT_BUTTON_POS = (int(X*0.05), int(X*0.45))
    MAX_SHOT_BUTTON_DATA = (MAX_SHOT_BUTTON_POS[0], MAX_SHOT_BUTTON_POS[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
    MAX_SHOT_BUTTON_COLOUR = (100,100,100) # Changed Later

    # Buy Shield Button #
    SHIELD_BUTTON_POS = (int(X*0.55), int(X*0.45))
    SHIELD_BUTTON_DATA = (SHIELD_BUTTON_POS[0], SHIELD_BUTTON_POS[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
    SHIELD_BUTTON_COLOUR = (100,100,100) # Changed Later

    # Current Score #
    scoreFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.07))
    scoreText = scoreFont.render(f"Score: {Player.score}", True, (0,255,255), (0,0,0))
    scoreTextbox = scoreText.get_rect()
    scoreTextbox.center = (int(X*0.5), int(Y*0.9))

    # Initialise Resume Button Variables # -> Player Sprite + Highlight Box
    playerShip = Player.SHIP_SPRITE
    shipCenter = (int(X*0.5), int(Y*0.7))
    resumeFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.03))
    textShade = 255
    textTicks = 0
    textShadeLimit = (50,255)
    resumeText = resumeFont.render("RESUME", True, (textShade,textShade,textShade), (0,0,0))
    resumeTextbox = resumeText.get_rect()
    resumeTextbox.center = (int(X*0.5), int(shipCenter[1] +Player.size*1.5))

    ## MAIN LOOP ##
    while True:
        ## INTER-FRAME VARIABLES & HANDLING ##
        SCREEN.fill(Colours.BACKGROUND_COLOUR)
        keys = py.key.get_pressed()
        Mouse.B1, Mouse.B2, Mouse.B3 = py.mouse.get_pressed()
        Mouse.leftClick, Mouse.rightClick = False, False
        Mouse.currentPos, Mouse.prevPos, Mouse.movement = Mouse.calculate_movement(py.mouse.get_pos(), Mouse.prevPos)
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Mouse.leftClick = True
                if event.button == 3:
                    Mouse.rightClick = True
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()

        ## DYNAMIC FADE ##
        if textTicks %2 == 0:
            textShade -= 4
            if textShade < textShadeLimit[0]:
                textShade = textShadeLimit[0]
                textTicks += 1
        if textTicks %2 == 1:
            textShade += 4
            if textShade > textShadeLimit[1]:
                textShade = textShadeLimit[1]
                textTicks += 1

        ## PRINT CURRENT SCORE ##
        SCREEN.blit(scoreText, scoreTextbox)

        ## DRAW AND MOVE STARS ##
        Stars.posY = Stars.handle_stars(SCREEN, Stars)

        ## DRAW PLAYER ##
        py.draw.line(SCREEN, (255,60,0), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.02))
        py.draw.line(SCREEN, (255,255,0), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.01))
        py.draw.line(SCREEN, (255,255,240), shipCenter, (shipCenter[0], 
            shipCenter[1] + int(X * 0.04) + random.randrange(int(X * 0.01))), int(X * 0.005))
        SCREEN.blit(playerShip, (shipCenter[0]-Player.halfSize, shipCenter[1]-Player.halfSize))

        ## PLAYER HIGHLIGHT BOX ## -> Resume button
        resumeText = resumeFont.render("RESUME", True, (textShade,textShade,textShade), (0,0,0))
        SCREEN.blit(resumeText, resumeTextbox)
        py.draw.rect(SCREEN, (textShade,textShade,textShade), 
            (int(shipCenter[0]-Player.halfSize*1.5), int(shipCenter[1]-Player.halfSize*1.5), int(Player.size*1.5), int(Player.size*1.8)), int(X*0.005 +1))
        if Mouse.leftClick:
            if int(shipCenter[0]-Player.halfSize*1.5) < Mouse.currentPos[0] < int(shipCenter[0]-Player.halfSize*1.5 + Player.size*1.5):
                if int(shipCenter[1]-Player.halfSize*1.5) < Mouse.currentPos[1] < int(shipCenter[1]-Player.halfSize*1.5 + Player.size*1.8):
                    break
        
        ## PRINT 'UPGRADES!'' ##
        upgradesTitleText = upgradesTitleFont.render("UPGRADES!", True, colour_loop_RGB(colourPointsRGB, loopLengthRGB, ticks%loopLengthRGB), (0,0,0))
        SCREEN.blit(upgradesTitleText, upgradesTitleTextbox)

        ## DETECT SHOP BUTTON CLICKS ##
        # Ammo #
        if AMMO_BUTTON_POS[0] < Mouse.currentPos[0] < AMMO_BUTTON_POS[0] +BUTTON_SIZE[0]:
            if AMMO_BUTTON_POS[1] < Mouse.currentPos[1] < AMMO_BUTTON_POS[1] +BUTTON_SIZE[1]:
                AMMO_BUTTON_COLOUR = (0,255,0)
            else:
                AMMO_BUTTON_COLOUR = (0,150,0)
        else:
            AMMO_BUTTON_COLOUR = (0,150,0)
        # Autofire #
        if Player.Upgrades.autoShoot:
            AUTOSHOOT_BUTTON_COLOUR = (100,100,100)
        else:
            if AUTOSHOOT_BUTTON_POS[0] < Mouse.currentPos[0] < AUTOSHOOT_BUTTON_POS[0] + BUTTON_SIZE[0]:
                if AUTOSHOOT_BUTTON_POS[1] < Mouse.currentPos[1] < AUTOSHOOT_BUTTON_POS[1] + BUTTON_SIZE[1]:
                    AUTOSHOOT_BUTTON_COLOUR = (0,255,0)
                else:
                    AUTOSHOOT_BUTTON_COLOUR = (0,150,0)
            else:
                AUTOSHOOT_BUTTON_COLOUR = (0,150,0)
        # Max Shots #
        if MAX_SHOT_BUTTON_POS[0] < Mouse.currentPos[0] < MAX_SHOT_BUTTON_POS[0] + BUTTON_SIZE[0]:
            if MAX_SHOT_BUTTON_POS[1] < Mouse.currentPos[1] < MAX_SHOT_BUTTON_POS[1] + BUTTON_SIZE[1]:
                MAX_SHOT_BUTTON_COLOUR = (0,255,0)
            else:
                MAX_SHOT_BUTTON_COLOUR = (0,150,0)
        else:
            MAX_SHOT_BUTTON_COLOUR = (0,150,0)
        # Shield #
        if Player.Upgrades.shield:
            SHIELD_BUTTON_COLOUR = (100,100,100)
        else:
            if SHIELD_BUTTON_POS[0] < Mouse.currentPos[0] < SHIELD_BUTTON_POS[0] + BUTTON_SIZE[0]:
                if SHIELD_BUTTON_POS[1] < Mouse.currentPos[1] < SHIELD_BUTTON_POS[1] + BUTTON_SIZE[1]:
                    SHIELD_BUTTON_COLOUR = (0,255,0)
                else:
                    SHIELD_BUTTON_COLOUR = (0,150,0)
            else:
                SHIELD_BUTTON_COLOUR = (0,150,0)


        ## DRAW UPGRADE BUTTONS ##
        # Ammo #
        py.draw.rect(SCREEN, AMMO_BUTTON_COLOUR, AMMO_BUTTON_DATA)
        # Autofire #
        py.draw.rect(SCREEN, AUTOSHOOT_BUTTON_COLOUR, AUTOSHOOT_BUTTON_DATA)
        # Max Shots #
        py.draw.rect(SCREEN, MAX_SHOT_BUTTON_COLOUR, MAX_SHOT_BUTTON_DATA)
        # Shield #
        py.draw.rect(SCREEN, SHIELD_BUTTON_COLOUR, SHIELD_BUTTON_DATA)

        ## UPDATE DISPLAY ##
        clock.tick(60)
        py.display.update()
        ticks += 1

    py.mouse.set_visible(0)
    return Stars.posY, py.time.get_ticks() # Return shuffled stars pos and time at end of script (beginning of next level)

def death_transition_screen(): # Transition into post-death screen / game summary
    ## INITIAL VARIABLES ##
    starMovement = X * 0.002
    font = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.03))
    while True:
        ## INTER-FRAME HANDLING & VARIABLES ##
        SCREEN.fill(Colours.BACKGROUND_COLOUR)
        keys = py.key.get_pressed()
        Mouse.B1, Mouse.B2, Mouse.B3 = py.mouse.get_pressed()
        Mouse.currentPos, Mouse.prevPos, Mouse.movement = Mouse.calculate_movement(py.mouse.get_pos(), Mouse.prevPos)
        Mouse.leftClick, Mouse.rightClick = False, False
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Mouse.leftClick = True
                if event.button == 3:
                    Mouse.rightClick = True
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()

        ## PRINT STAR BACKGROUND ##
        Stars.posY = Stars.handle_stars(SCREEN, Stars, starMovement)  

        ## UPDATE SCREEN + INTER-FRAME VARIABLES ##
        clock.tick(50)
        py.display.update() 
        starMovement *= 0.98
        if starMovement < X*0.0001:
            break

    ## CREATE DARKENED STAR BACKGROUND ##
    tempSurface = py.Surface((X, Y))
    tempSurface.fill(Colours.BACKGROUND_COLOUR)
    tempSurface.set_alpha(150)
    SCREEN.blit(tempSurface, (0, 0))
    STAR_BACKGROUND = SCREEN.convert()

   	## RETURN VARIABLES ##
    return Stars.posY, STAR_BACKGROUND
    
def post_death_screen(): # Death Screen; Shows game stats, score, and leaderboard
    ## ENABLE MOUSE VISIBILITY ##
    py.mouse.set_visible(1) 

    ## HANDLE HIGHSCORE FILES ##
    highscores, highscoresLen = handle_highscores()

    ## INITIAL VARIABLES / FONTS ##
    mainTextColour = (200,255,200)
    ticks = 0
    normalFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.03))
    titleLeaderboardFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.06))
    titleScoreFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.05))
    destroyedTitleFont = py.font.Font(os.path.join('Fonts', 'arcadeText.ttf'), int(X*0.04))
    destroyedTextFont = normalFont
    loopLengthRGB = 250
    colourPointsRGB = [(255,0,0), (255,0,255), (0,0,255), (0,255,255), (0,255,0), (255,255,0)]
    textShade = 255
    textTicks = 0
    textShadeLimit = (50,255)

    scoreText = titleScoreFont.render(f"You scored: {Player.score}", True, (textShade,textShade,textShade), (0,0,0))
    scoreTextbox = scoreText.get_rect()
    scoreTextbox.center = (int(X*0.5), int(Y*0.1))

    leaderboardTitleText = titleLeaderboardFont.render("Leaderboard", True, colour_loop_RGB(colourPointsRGB, loopLengthRGB, ticks%loopLengthRGB), (0,0,0))
    leaderboardTitleTextbox = leaderboardTitleText.get_rect()
    leaderboardTitleTextbox.center = (int(X*0.5), int(Y*0.2))

    ## for below; ERROR -> 'pygame.surface object is not iterable'  #-> (And so I made them manualy, the bane of my existance)
    #highscoresPositioningText = []
    #for i in range(1,11):
    #    highscoresPositioningText.extend(normalFont.render(f"{i} |", True, mainTextColour, (0,0,0)))

    if highscoresLen >= 1:
        HSPos1ST = normalFont.render(f"{highscores[0]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 2:
        HSPos2ST = normalFont.render(f"{highscores[1]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 3:
        HSPos3ST = normalFont.render(f"{highscores[2]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 4:
        HSPos4ST = normalFont.render(f"{highscores[3]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 5:
        HSPos5ST = normalFont.render(f"{highscores[4]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 6:
        HSPos6ST = normalFont.render(f"{highscores[5]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 7:
        HSPos7ST = normalFont.render(f"{highscores[6]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 8:
        HSPos8ST = normalFont.render(f"{highscores[7]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 9:
        HSPos9ST = normalFont.render(f"{highscores[8]}", True, mainTextColour, (0,0,0))
    if highscoresLen >= 10:
        HSPos10ST = normalFont.render(f"{highscores[9]}", True, mainTextColour, (0,0,0))

    HSPos1T = normalFont.render("1 |", True, mainTextColour, (0,0,0))
    HSPos2T = normalFont.render("2 |", True, mainTextColour, (0,0,0))
    HSPos3T = normalFont.render("3 |", True, mainTextColour, (0,0,0))
    HSPos4T = normalFont.render("4 |", True, mainTextColour, (0,0,0))
    HSPos5T = normalFont.render("5 |", True, mainTextColour, (0,0,0))
    HSPos6T = normalFont.render("6 |", True, mainTextColour, (0,0,0))
    HSPos7T = normalFont.render("7 |", True, mainTextColour, (0,0,0))
    HSPos8T = normalFont.render("8 |", True, mainTextColour, (0,0,0))
    HSPos9T = normalFont.render("9 |", True, mainTextColour, (0,0,0))
    HSPos10T = normalFont.render("10|", True, mainTextColour, (0,0,0))

    # User Score On Leaderboard?
    scoreOnLeaderboard = False
    for score in highscores:
        if Player.score == score:
            scoreOnLeaderboard = True
            onLeaderboardText = normalFont.render(f"You're on the leaderboard!", True, (textShade,textShade,textShade), (0,0,0))
            onLeaderboardTextbox = onLeaderboardText.get_rect()
            onLeaderboardTextbox.center = (int(X*0.5), int(Y*0.57))
            break

    # Num Of Destroyed Enemies
    destroyedTitleText = destroyedTitleFont.render(f"Enemies Destroyed", True, mainTextColour, (0,0,0))
    destroyedTitleTextbox = destroyedTitleText.get_rect()
    destroyedTitleTextbox.center = (int(X*0.5), int(Y*0.63))
    destroyedAsteroidsText = destroyedTextFont.render(f"Asteroids | {Player.destroyedAsteroids}", True, mainTextColour, (0,0,0))
    destroyedShipsText =     destroyedTextFont.render(f"Ships     | {Player.destroyedShips}", True, mainTextColour, (0,0,0))

    ## CREATE BUTTONS ##
    # Universal
    BUTTONFONT = destroyedTitleFont
    BUTTONSIZE = (int(X*0.3), int(Y*0.1))
    BUTTON_BACKGROUND_ALPHA = 150
    BUTTON_SELECTED_ALPHA = 255

    # Continue Button
    continueButton = py.Surface(BUTTONSIZE)
    continueButton.fill((0,200,0))
    continueButton.set_alpha(BUTTON_BACKGROUND_ALPHA)
    continueButtonPos = (int(X*0.1), int(Y*0.8))
    continueButtonRect = py.Rect(continueButtonPos, BUTTONSIZE)
    continueButtonText = BUTTONFONT.render(f"RETRY", True, (255,255,255), (0,200,0))
    continueButtonTextbox = continueButtonText.get_rect()
    continueButtonTextbox.center = (int(BUTTONSIZE[0]*0.5), int(BUTTONSIZE[1]*0.5))
    continueButton.blit(continueButtonText, continueButtonTextbox)

    # Quit Button
    quitButton = py.Surface(BUTTONSIZE)
    quitButton.fill((200,0,0))
    quitButton.set_alpha(BUTTON_BACKGROUND_ALPHA)
    quitButtonPos = (int(X*0.6), int(Y*0.8))
    quitButtonRect = py.Rect(quitButtonPos, BUTTONSIZE)
    quitButtonText = BUTTONFONT.render(f"QUIT", True, (255,255,255), (200,0,0))
    quitButtonTextbox = quitButtonText.get_rect()
    quitButtonTextbox.center = (int(BUTTONSIZE[0]*0.5), int(BUTTONSIZE[1]*0.5))
    quitButton.blit(quitButtonText, quitButtonTextbox)

    ## DEFINE SCREEN UPDATE POSITIONS ##
    updateRects = [scoreTextbox, leaderboardTitleTextbox, quitButtonRect, continueButtonRect]
    if scoreOnLeaderboard:
    	updateRects.append(onLeaderboardTextbox)

    ## RESTART INTRO MUSIC ##
    py.mixer.music.stop()
    py.mixer.music.load(os.path.join('Sounds', 'music', 'main_page_music.wav'))
    py.mixer.music.play(-1)
    while True:
        ## INTER-FRAME HANDLING & VARIABLES ##
        SCREEN.blit(STAR_BACKGROUND, (0,0)) #-> Sets stationary stars with transparent black overlay as background
        keys = py.key.get_pressed()
        Mouse.B1, Mouse.B2, Mouse.B3 = py.mouse.get_pressed()
        Mouse.currentPos, Mouse.prevPos, Mouse.movement = Mouse.calculate_movement(py.mouse.get_pos(), Mouse.prevPos)
        Mouse.leftClick, Mouse.rightClick = False, False
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Mouse.leftClick = True
                if event.button == 3:
                    Mouse.rightClick = True
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
        if keys[py.K_ESCAPE]:
            py.display.quit()
            py.quit()
        if keys[py.K_RETURN]:
            break

        ## DETECT MOUSE COLLISIONS ##
        # BUTTONS #
        if continueButtonPos[1] < Mouse.currentPos[1] < continueButtonPos[1] + BUTTONSIZE[1]: 
            #-> QUIT and CONTINUE buttons share the same y-pos and size, thus only need to detect this once for optimisation
            if continueButtonPos[0] < Mouse.currentPos[0] < continueButtonPos[0] + BUTTONSIZE[0]:
                continueButton.set_alpha(BUTTON_SELECTED_ALPHA)
                if Mouse.leftClick:
                	break
            else:
                continueButton.set_alpha(BUTTON_BACKGROUND_ALPHA)
            if quitButtonPos[0] < Mouse.currentPos[0] < quitButtonPos[0] + BUTTONSIZE[0]:
                quitButton.set_alpha(BUTTON_SELECTED_ALPHA)
                if Mouse.leftClick:
                	py.display.quit()
                	py.quit()
            else:
                quitButton.set_alpha(BUTTON_BACKGROUND_ALPHA)
        else:
            continueButton.set_alpha(BUTTON_BACKGROUND_ALPHA)
            quitButton.set_alpha(BUTTON_BACKGROUND_ALPHA)

        ## DYNAMIC TEXT CHANGE -> White Fade In-Out ##
        if textTicks %2 == 0:
            textShade -= 4
            if textShade < textShadeLimit[0]:
                textShade = textShadeLimit[0]
                textTicks += 1

        if textTicks %2 == 1:
            textShade += 4
            if textShade > textShadeLimit[1]:
                textShade = textShadeLimit[1]
                textTicks += 1

        ## DISPLAY TEXT ##
        # Player Score
        scoreText = titleScoreFont.render(f"You scored: {Player.score}", True, (textShade,textShade,textShade), (0,0,0))
        SCREEN.blit(scoreText, scoreTextbox)

        # Leaderboard Title
        leaderboardTitleText = titleLeaderboardFont.render("Leaderboard", True, colour_loop_RGB(colourPointsRGB, loopLengthRGB, ticks%loopLengthRGB), (0,0,0))

        # Leaderboard Positions
        SCREEN.blit(leaderboardTitleText, leaderboardTitleTextbox)
        SCREEN.blit(HSPos1T, (int(X*0.2), int(Y*0.25)))
        SCREEN.blit(HSPos2T, (int(X*0.2), int(Y*0.28)))
        SCREEN.blit(HSPos3T, (int(X*0.2), int(Y*0.31)))
        SCREEN.blit(HSPos4T, (int(X*0.2), int(Y*0.34)))
        SCREEN.blit(HSPos5T, (int(X*0.2), int(Y*0.37)))
        SCREEN.blit(HSPos6T, (int(X*0.2), int(Y*0.40)))
        SCREEN.blit(HSPos7T, (int(X*0.2), int(Y*0.43)))
        SCREEN.blit(HSPos8T, (int(X*0.2), int(Y*0.46)))
        SCREEN.blit(HSPos9T, (int(X*0.2), int(Y*0.49)))
        SCREEN.blit(HSPos10T, (int(X*0.2), int(Y*0.52)))

        # Leaderboard Scores
        if highscoresLen >= 1:
            SCREEN.blit(HSPos1ST, (int(X*0.35), int(Y*0.25)))
        if highscoresLen >= 2:
            SCREEN.blit(HSPos2ST, (int(X*0.35), int(Y*0.28)))
        if highscoresLen >= 3:
            SCREEN.blit(HSPos3ST, (int(X*0.35), int(Y*0.31)))
        if highscoresLen >= 4:
            SCREEN.blit(HSPos4ST, (int(X*0.35), int(Y*0.34)))
        if highscoresLen >= 5:
            SCREEN.blit(HSPos5ST, (int(X*0.35), int(Y*0.37)))
        if highscoresLen >= 6:
            SCREEN.blit(HSPos6ST, (int(X*0.35), int(Y*0.40)))
        if highscoresLen >= 7:
            SCREEN.blit(HSPos7ST, (int(X*0.35), int(Y*0.43)))
        if highscoresLen >= 8:
            SCREEN.blit(HSPos8ST, (int(X*0.35), int(Y*0.46)))
        if highscoresLen >= 9:
            SCREEN.blit(HSPos9ST, (int(X*0.35), int(Y*0.49)))
        if highscoresLen >= 10:
            SCREEN.blit(HSPos10ST, (int(X*0.35), int(Y*0.52)))
        # User On Leaderboard?
        if scoreOnLeaderboard:
            onLeaderboardText = normalFont.render(f"You're on the leaderboard!", True, (textShade,textShade,textShade), (0,0,0))
            SCREEN.blit(onLeaderboardText, onLeaderboardTextbox)
        # Game Stats / Destroyed Enemies
        SCREEN.blit(destroyedTitleText, destroyedTitleTextbox)
        SCREEN.blit(destroyedAsteroidsText, (int(X*0.25), int(Y*0.66)))
        SCREEN.blit(destroyedShipsText, (int(X*0.25), int(Y*0.69)))

        ## CONTINUE & QUIT BUTTONS ##
        SCREEN.blit(continueButton, continueButtonPos)
        SCREEN.blit(quitButton, quitButtonPos)

        ## UPDATE SCREEN + INTER-FRAME VARIABLES ##
        clock.tick(50)
        #py.display.update()
        py.display.update(updateRects)
        ticks += 1

class Stars: # Background Stars
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
            py.draw.rect(SURFACE, (200,200,200), (Stars.posX[i], int(Stars.posY[i]), int(Stars.depth[i]), int(Stars.depth[i])))
            # In case of depreciation of auto int() with pygame vectors:
            #py.draw.rect(SURFACE, (255,255,255), (int(Stars.posX[i]), int(Stars.posY[i]), int(Stars.depth[i]), int(Stars.depth[i])))
        return Stars.posY

class Mouse: # All mouse related variables / input
    currentPos = (0,0)                      # Current pos of mouse expressed as (x, y)
    prevPos = (0,0)                         # Pos of mouse last frame expressed as (x, y)
    movement = (0,0)                        # The difference is x & y pos of mouse between frames expressed as (x, y)
    B1, B2, B3 = False, False, False        # Mouse held down? -> B1 = left button   B2 = middle button   B3 = right button
    leftClick, rightClick = False, False    # Initial click    -> Only active for frame in which click occurs
    clickPos = (0,0)                        # Pos of last click expressed as (x, y)     

    def calculate_movement(currentPos, prevPos): # Returns related mouse pos variables
        x1, y1 = currentPos
        x2, y2 = prevPos
        posDifference = (x1 - x2, y1 - y2)
        prevPos = currentPos
        return currentPos, prevPos, posDifference

class Colours: # All colours (Preferabaly RGB format)
    BLACK        = (  0,   0,   0)
    WHITE        = (255, 255, 255)
    RED          = (255,   0,   0)
    GREEN        = (  0, 255,   0)
    BLUE         = (  0,   0, 255)
    GREY         = (170, 170, 170)
    BACKGROUND_COLOUR = (0, 0, 0) 
    PLAYER_LASER_COLOUR = (255,100,50)

class Player: # Player variables
    score = 0
    size = int(X * 0.07)
    halfSize = int(size * 0.5)
    destroyedAsteroids = 0
    destroyedShips = 0
    SHIP_SPRITE = py.transform.scale(py.image.load(os.path.join('Sprites', 'player.png')).convert_alpha(), (size, size))
    DEATH_EXPLOSION = py.transform.scale(py.image.load(os.path.join('Sprites', 'death_explosion.png')).convert_alpha(), (int(size*2), int(size*2)))
    class Ammo:
        lasers = 100 # Even if you change it to zero it does nothing
        bombs = 0
    class Upgrades:
        autoShoot = False
        maxLasers = 1
        shield = False

    def draw_player():
        py.draw.line(SCREEN, (255,60,0), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.02))
        py.draw.line(SCREEN, (255,255,0), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.02))), int(random.randrange(int(X * 0.01)) + X * 0.01))
        py.draw.line(SCREEN, (255,255,240), Mouse.currentPos, (Mouse.currentPos[0], 
            Mouse.currentPos[1] + int(X * 0.04) + random.randrange(int(X * 0.01))), int(X * 0.005))
        SCREEN.blit(Player.SHIP_SPRITE, (Mouse.currentPos[0] - Player.halfSize, 
            Mouse.currentPos[1] - Player.halfSize))

    def detect_collisions():
        for index, (APosX, APosY, ASize, ASprite) in enumerate(Enemies.Asteroids.data):
            if distance((Mouse.currentPos), (int(APosX + ASize*0.5), int(APosY + ASize*0.5))) < ASize*0.5 + Player.halfSize:
                del Enemies.Asteroids.data[index]
                return True
                break
        
    class Lasers:
        pos = []
        length = int(Y * 0.05)
        width = int(X * 0.005) + 1
        moveStep = int(Y * 0.03)

        def handle_lasers(Lasers, Enemies):
            # Move Lasers & Delete Offscreen
            global Player
            tempList = []
            for x, y in Lasers.pos:
                if not (y - Lasers.moveStep < 0):
                    tempList.append((x, y - Lasers.moveStep))
                else:
                    Player.score -= 5
            Lasers.pos = tempList[:]

            # Print Lasers
            for i in range(len(Lasers.pos)):
                py.draw.line(SCREEN, Colours.PLAYER_LASER_COLOUR, (Lasers.pos[i]),
                 (Lasers.pos[i][0], Lasers.pos[i][1] - Lasers.length), Lasers.width)

            return Lasers, Enemies

class Enemies: # All enemy variables (Asteroids, ships, etc)

    class Asteroids:
        initialSize = int(X * 0.1)
        initialSpeed = int(X * 0.005) + 1
        asteroid_1 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_1.png')).convert_alpha(), (initialSize, initialSize))
        asteroid_2 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_2.png')).convert_alpha(), (initialSize, initialSize))
        asteroid_3 = py.transform.scale(py.image.load(os.path.join('Sprites', 'asteroid_3.png')).convert_alpha(), (initialSize, initialSize))
        data = []    # X, Y, Size, Sprite

        def move_and_print(asteroidData):
            tempList = []
            for x, y, size, sprite in asteroidData:
                newY = y + Enemies.Asteroids.initialSpeed * (1 + difficulty * 0.1)
                if not newY > Y:
                    tempList.append((x, newY, size, sprite))
                    SCREEN.blit(sprite, (x, int(newY)))
            return tempList

        def create_new():
            size = int(Enemies.Asteroids.initialSize * ((random.randrange(10) + 5) / 10))
            randSelect = random.randrange(3)
            if randSelect == 0:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_1, (size, size))
            elif randSelect == 1:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_2, (size, size))
            else:
                sprite = py.transform.scale(Enemies.Asteroids.asteroid_3, (size, size))
            return (
                random.randrange(X + Enemies.Asteroids.initialSize) - Enemies.Asteroids.initialSize, # X
                -size,                                                                           # Y
                size,                                                                            # Size
                sprite)                                                                          # Scaled Sprite # Class for enemies (Asteroids, ships, etc)

    # This is where Xavier steps in to do his work at 4:39am
    class enemyShips:
        initialShipSize = int(X * 0.1)
        initialShipSpeed = int(X * 0.005) + 1
        pirate2 = py.transform.scale(py.image.load(os.path.join('Sprites', 'pirate2.png')).convert_alpha(), (initialShipSize, initialShipSize))
        shipData = []

        def spawnEnemyShip():
            size = int(Enemies.EnShips.initialShipSize)
            return py.transform.scale(Enemies.EnShips.pirate2, (size, size))

class Sounds: # Class to store all game music and SFX
    playerLaser = py.mixer.Sound(os.path.join("Sounds", "player_sounds", "player_laser.wav"))
    hyperdriveExit = py.mixer.Sound(os.path.join("Sounds", "player_sounds", "hyperdrive_exit.wav"))
    playerDeathExplosion = py.mixer.Sound(os.path.join("Sounds", "player_sounds", "player_death_explosion.wav"))
    enemyShipExplosion = py.mixer.Sound(os.path.join("Sounds", "enemy_ship_explosion.wav"))
    asteroidExplosions = [py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_1.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_2.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_3.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_4.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_5.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_6.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_7.wav")),
                            py.mixer.Sound(os.path.join("Sounds", "asteroid_explosions", "explosion_8.wav"))
                        ]
    #py.mixer.music.load("music.wav") #-> Loads a music file
    #py.mixer.music.play(-1) #-> Plays music. input specifies repeats. -1 specifies repeat forever
    #pygame.mixer.music.pause() #-> Pauses music
    #pygame.mixer.music.upause() #-> Unpauses music
    #py.mixer.music.stop() #-> Stops music
    #soundEffect = py.mixer.Sound("sound.wav") #-> Creates a sound effect variable
    #py.mixer.Sound.play(soundEffect) #-> Plays sound effect 

shop_screen()

## LOOP TO ALLOW REPLAY ##
firstRun = True
endLevel = False
while True:
    ## VARIABLE RESETS ## - Attempted resets via saving and loading a deepcopy of classes but ran into multiple issues
    # Player Class
    Player.score = 0
    Player.destroyedAsteroids = 0
    Player.destroyedShips = 0
    Player.Ammo.lasers = 100
    Player.Ammo.bombs = 0
    Player.Upgrades.autoShoot = False
    Player.Upgrades.maxLasers = 1
    Player.Upgrades.shield = False
    Player.Lasers.pos = []
    # Enemies Class
    Enemies.Asteroids.data = []
    # Difficulty
    difficulty = 0

    ## PRE-GAME START / INTRO SCREENS ##
    Stars.posY = intro_screen(Player.SHIP_SPRITE) 
    Stars.posX = intro_hyperdrive_animation(Stars, Player, 7.3)
    levelLength = 2000 # in ms
    levelStartTime = py.time.get_ticks()
    ## MAIN GAME LOOP ##
    while True:
        ## INTER-FRAME VARIABLES & HANDLING ##
        if True:
            SCREEN.fill(Colours.BACKGROUND_COLOUR)
            keys = py.key.get_pressed()
            Mouse.B1, Mouse.B2, Mouse.B3 = py.mouse.get_pressed()
            Mouse.leftClick, Mouse.rightClick = False, False
            Mouse.currentPos, Mouse.prevPos, Mouse.movement = Mouse.calculate_movement(py.mouse.get_pos(), Mouse.prevPos)
            time = py.time.get_ticks()
            for event in py.event.get():
                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Mouse.leftClick = True
                        Mouse.clickPos = Mouse.currentPos
                    if event.button == 3:
                        Mouse.rightClick = True
                        Mouse.clickPos = Mouse.currentPos
                if event.type == py.QUIT:
                    py.display.quit()
                    py.quit()
            if keys[py.K_ESCAPE]:
                py.display.quit()
                py.quit()

        ## CALCULATE AND DRAW BACKGROUND STARS ##
        Stars.posY = Stars.handle_stars(SCREEN, Stars)

        ## ADD AND DRAW ENEMIES ## - Asteroids
        if not endLevel:
            if random.randrange(41+ 2*difficulty) > 39:
                Enemies.Asteroids.data.append(Enemies.Asteroids.create_new())
        Enemies.Asteroids.data = Enemies.Asteroids.move_and_print(Enemies.Asteroids.data)

        ## PLAYER COLLISIONS WITH ENVIRONMENT ## - Kills Player
        if Player.detect_collisions(): #If a collision happens, delete object it collides with and runs specified script
            if Player.Upgrades.shield:
                Player.Upgrades.shield = False
            else:
                SCREEN.blit(Player.DEATH_EXPLOSION, (Mouse.currentPos[0]-Player.size, Mouse.currentPos[1]-Player.size))
                #DEATHFRAME = SCREEN.convert()
                py.mixer.Sound.play(Sounds.playerDeathExplosion)
                py.mixer.music.stop()
                py.display.update()
                #SCREEN.blit(DEATHFRAME, (0,0))
            break # -> Exits main loop, goto score screen

        ## PLAYER SHOOTS LASERS ##
        if Player.Ammo.lasers > 0:
            if len(Player.Lasers.pos) < Player.Upgrades.maxLasers:
                if Player.Upgrades.autoShoot:
                    if Mouse.B1:
                        Player.Lasers.pos.append(Mouse.currentPos)
                        py.draw.circle(SCREEN, (255,0,0), (Mouse.currentPos[0], Mouse.currentPos[1]-Player.halfSize), int(X*0.01 +1))
                        py.draw.circle(SCREEN, (255,200,200), (Mouse.currentPos[0], Mouse.currentPos[1]-Player.halfSize), int(X*0.008 +1))
                        Player.Ammo.lasers -= 1
                        py.mixer.Sound.play(Sounds.playerLaser)
                else:
                    if Mouse.leftClick:
                        Player.Lasers.pos.append(Mouse.currentPos)
                        py.draw.circle(SCREEN, (255,0,0), (Mouse.currentPos[0], Mouse.currentPos[1]-Player.halfSize), int(X*0.01 +1))
                        py.draw.circle(SCREEN, (255,200,200), (Mouse.currentPos[0], Mouse.currentPos[1]-Player.halfSize), int(X*0.008 +1))
                        Player.Ammo.lasers -= 1
                        py.mixer.Sound.play(Sounds.playerLaser)
        Player.Lasers, Enemies = Player.Lasers.handle_lasers(Player.Lasers, Enemies)

        ## PLAYER'S LASER COLLISIONS ##
        indexOffset = 0
        for i in range(len(Player.Lasers.pos)):
            laserTopPos = (Player.Lasers.pos[i - indexOffset][0], Player.Lasers.pos[i - indexOffset][1] - Player.Lasers.length)

            for n in range(len(Enemies.Asteroids.data)):
                try: # TEMPORARY BUG FIX
                    asteroidSize = Enemies.Asteroids.data[n - indexOffset][2]# this line has a problem
                except IndexError:
                    print("\nSomething broke.\n")
                    #raise idiot

                asteroidPosX, asteroidPosY = Enemies.Asteroids.data[n-indexOffset][0:2]
                asteroidCenter = ((asteroidPosX + asteroidSize * 0.5), (asteroidPosY + asteroidSize * 0.5))

                if distance(asteroidCenter, laserTopPos) < Enemies.Asteroids.data[n - indexOffset][2] * 0.6:
                    py.draw.circle(SCREEN, (255,200,200), laserTopPos, int(Y * 0.01))
                    py.draw.circle(SCREEN, Colours.RED, laserTopPos, int(Y * 0.007))

                    del Player.Lasers.pos[i - indexOffset], Enemies.Asteroids.data[n - indexOffset]
                    indexOffset += 1

                    Player.score += 10
                    Player.destroyedAsteroids += 1

                    py.mixer.Sound.play(Sounds.asteroidExplosions[random.randrange(len(Sounds.asteroidExplosions))])

                    break

        ## PRINT SCORE TEST ##
        SCREEN.blit(py.font.Font(None, int(X*0.05)).render(f"Score: {Player.score}", True, (255,255,255), (100,100,100)), (int(X*0.05), int(X*0.05)))

        ## DRAW PLAYER ##
        Player.draw_player()

        ## UPDATE SCREEN ##
        clock.tick(60)
        py.display.update() 

        ## DETECT END OF LEVEL ##
        if endLevel:
            if len(Enemies.Asteroids.data) == 0:
            	endLevel = False
            	Stars.posX = hyperdrive_animation(Stars, Player)
            	Stars.posY, levelStartTime = shop_screen()
            	difficulty += 1
        elif time > levelStartTime+ levelLength: 
        	endLevel = True

    ## END SCREEN + HIGHSCORES ##
    Stars.posY, STAR_BACKGROUND = death_transition_screen()
    post_death_screen()

























