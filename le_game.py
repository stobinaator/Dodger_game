import pygame, random, sys, os
from pygame.locals import *



WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 4
POWERUPSIZE = 20
SPEEDSIZE = 20
DIRECTORY = os.path.dirname(__file__)
HS_FILE = 'highscore.txt'

baddieRates = {'one' : {'ADDNEWBADDIERATE1':25,'ADDNEWGOODIERATE1':25}, # until 500
               'two' : {'ADDNEWBADDIERATE2':20,'ADDNEWGOODIERATE2':28}, # above 500
               'three' : {'ADDNEWBADDIERATE3':15,'ADDNEWGOODIERATE3':31}, # above 1500
               'four' : {'ADDNEWBADDIERATE4':13,'ADDNEWGOODIERATE4':33}, # above 3000
               'five' : {'ADDNEWBADDIERATE5':11,'ADDNEWGOODIERATE5':35}, # above 5000
               'six' : {'ADDNEWBADDIERATE6':9,'ADDNEWGOODIERATE6':38}, # above 7000
               'seven' : {'ADDNEWBADDIERATE7':6,'ADDNEWGOODIERATE7':41}, # above 10k
               }

PLAYERMOVERATE = 3

# set up game, the window, the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Antisocial')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 48)


# sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('bird.mp3')

# images
PLAYERS_DIR = "players/"
baddies_list = []
goodies_list = []
for dirpath, dirnames, files in os.walk(os.path.abspath(PLAYERS_DIR)):
    if dirpath.endswith('bad'):
        for file in files:
            if file.startswith('baddie'):
                continue
            baddies_list.append(PLAYERS_DIR + 'bad/' + file)
    if dirpath.endswith('good'):
        for file in files:
            goodies_list.append(PLAYERS_DIR + 'good/' + file)


playerImage = pygame.image.load(PLAYERS_DIR +'player.png').convert()
playerRect = playerImage.get_rect()

powerUpImage = pygame.image.load(PLAYERS_DIR + 'powerups/' + 'red.png').convert_alpha()
speedUpImage = pygame.image.load(PLAYERS_DIR + 'powerups/' + 'flash.png').convert_alpha()


def load_data(DIRECTORY, HS_FILE):
    with open(os.path.join(DIRECTORY, HS_FILE), 'r') as f:
        try:
            highscore = float(f.read())
        except:
            highscore = 0
    return highscore


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
                return


def waitForPlayerToPressKey2():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitSpeedUp(playerRect, speedUp):
    for s in speedUp[:]:
        if playerRect.colliderect(s['rect']):
            speedUp.remove(s)
            return True
    return False

def playerHasHitPowerUp(playerRect, powerUp):
    for p in powerUp[:]:
        if playerRect.colliderect(p['rect']):
            powerUp.remove(p)
            return True
    return False


def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def playerHasHitGoodie(playerRect, goodies):
    for g in goodies[:]:
        if playerRect.colliderect(g['rect']):
            goodies.remove(g)
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def moveFigureDown(whoever, score, reverseCheat, slowCheat):
    for w in whoever:
        if not reverseCheat and not slowCheat:
            w['rect'].move_ip(0, w['speed'])
        elif reverseCheat:
            w['rect'].move_ip(0, -5)
            score -= 0.6
        elif slowCheat:
            w['rect'].move_ip(0, 1)
            score -= 0.3
    return score


def delFigurePastBottom(whoever):
    for w in whoever[:]:
        if w['rect'].top > WINDOW_HEIGHT:
            whoever.remove(w)

def addNewSpeedUp(image):
    speedSize = SPEEDSIZE
    newFigure = {'rect' : pygame.Rect(random.randint(0, WINDOW_WIDTH - speedSize), 
                                      random.randint(0, WINDOW_HEIGHT - speedSize), speedSize, speedSize),
                'surface' : pygame.transform.scale(image, (speedSize, speedSize)),
                 }
    return newFigure

def addNewPowerUp(image):
    powerupSize = POWERUPSIZE
    newFigure = {'rect' : pygame.Rect(random.randint(0, WINDOW_WIDTH - powerupSize), 
                                      random.randint(0, WINDOW_HEIGHT - powerupSize), powerupSize, powerupSize),
                'surface' : pygame.transform.scale(image, (powerupSize, powerupSize)),
                 }
    return newFigure


def addNewFigure(image):   
    baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
    newFigure = {'rect' : pygame.Rect(random.randint(0,
                        WINDOW_WIDTH - baddieSize), 0 - baddieSize,
                        baddieSize, baddieSize),
                'speed' : random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface' : pygame.transform.scale(image,
                                (baddieSize, baddieSize)),
                 }
    return newFigure


def movePlayerAround(moveLeft, moveRight, moveUp, moveDown, playerRect, PLAYERMOVERATE):
    # move the player around
    if moveLeft:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if playerRect.centerx - 10 < 0:
                playerRect.x = WINDOW_WIDTH - 10
                playerRect.y = playerRect.y
    if moveRight:
            playerRect.move_ip(PLAYERMOVERATE, 0)
            if playerRect.centerx + 10 > WINDOW_WIDTH:
                playerRect.x = 10
                playerRect.y = playerRect.y
    if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
    if moveDown and playerRect.bottom < WINDOW_HEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)



def main_menu():
    # start screen
    windowSurface.fill(BACKGROUNDCOLOR)
    drawText('∆ Antisocial ∆', font, windowSurface, (WINDOW_WIDTH/3) , (WINDOW_HEIGHT/3))
    hs = load_data(DIRECTORY, HS_FILE)
    drawText(f'HIGH SCORE: {hs}', font, windowSurface, (WINDOW_WIDTH/3) - 50, (WINDOW_HEIGHT/3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey2()
    main_menu2()
    return hs

TEXT_POSITION = 70

def main_menu2():
    windowSurface.fill(BACKGROUNDCOLOR)
    drawText('There are 7 stages',
         font, windowSurface, TEXT_POSITION, (WINDOW_HEIGHT/4))
    drawText('Use arrows or wasd',
         font, windowSurface, TEXT_POSITION, (WINDOW_HEIGHT/4) + 50)
    drawText('X to slow down time',
         font, windowSurface, TEXT_POSITION, (WINDOW_HEIGHT/4) + 100)
    drawText('Y to make them fly backwards',
         font, windowSurface, TEXT_POSITION, (WINDOW_HEIGHT/4) + 150)
    drawText('M to toogle music on/off',
         font, windowSurface, TEXT_POSITION, (WINDOW_HEIGHT/4) + 200)
    drawText('Press a key to start', font, windowSurface, TEXT_POSITION,
                                                     (WINDOW_HEIGHT/4) + 250)
    pygame.display.update()
    waitForPlayerToPressKey()   


def addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies, goodies, 
                 wordNr,wordNr2, badImg, goodieImage, score):
    
    if baddieAddCounter >= baddieRates[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
        baddieAddCounter = baddieRates[wordNr]['ADDNEWBADDIERATE' + wordNr2]
        if baddieAddCounter == baddieRates[wordNr]['ADDNEWBADDIERATE' + wordNr2]:
             baddieAddCounter = 0
             newBaddie = addNewFigure(badImg)
             baddies.append(newBaddie)
    if goodieAddCounter >= baddieRates[wordNr]['ADDNEWGOODIERATE' + wordNr2]:
        goodieAddCounter = baddieRates[wordNr]['ADDNEWGOODIERATE' + wordNr2]
        if goodieAddCounter == baddieRates[wordNr]['ADDNEWGOODIERATE' + wordNr2]:   
            goodieAddCounter = 0
            newGoodie = addNewFigure(goodieImage)
            goodies.append(newGoodie)
    return goodies, baddies, goodieAddCounter, baddieAddCounter, score



def checkScore(baddieAddCounter, goodieAddCounter, score, baddies, goodies, baddieImage, randomBaddieImage, goodieImage, baddieRates):

    if score > 10000:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'seven', '7', randomBaddieImage, goodieImage, score)

    elif score > 7000:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'six', '6', randomBaddieImage, goodieImage, score)

    elif score > 5000:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'five', '5', randomBaddieImage, goodieImage, score) 

    elif score > 3000:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'four', '4', randomBaddieImage, goodieImage, score)

    elif score > 1500:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'three', '3', randomBaddieImage, goodieImage, score)
        
    elif score > 500:
        return addNewBaddiesAndGoodies(baddieAddCounter, goodieAddCounter, baddieRates, baddies,
                                        goodies, 'two', '2',  randomBaddieImage, goodieImage, score)
        
    elif score < 500:
        if baddieAddCounter == baddieRates['one']['ADDNEWBADDIERATE1']:
            baddieAddCounter = 0
            newBaddie = addNewFigure(baddieImage)
            baddies.append(newBaddie)

        if goodieAddCounter == baddieRates['one']['ADDNEWGOODIERATE1']:
            goodieAddCounter = 0
            newGoodie = addNewFigure(goodieImage)
            goodies.append(newGoodie)

    return goodies, baddies, goodieAddCounter, baddieAddCounter, score


def addNewSpeedUpToList(iteration, speedups, speedUpImage):
    if iteration % 600 == 0:
        newSpeedUp = addNewPowerUp(speedUpImage)
        speedups.append(newSpeedUp)
    return speedups

def addNewPowerUpToList(iteration, powerups, powerupImage):
    if iteration % 300 == 0:
        newPowerUp = addNewPowerUp(powerUpImage)
        powerups.append(newPowerUp)

    return powerups


def game_over(score, lastScore, topScore, hs):
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH /3), (WINDOW_HEIGHT / 3))
    drawText(f'Score: {round(score,2)}', font, windowSurface,
                 (WINDOW_WIDTH / 3), (WINDOW_HEIGHT / 3) + 40)
    drawText('Press a key to play again.', font, windowSurface,
                 (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 120)
    

    if score > topScore:
        topScore = score

    if score > hs:
        hs = score
        drawText('NEW HIGH SCORE!', font, windowSurface,
                  (WINDOW_WIDTH / 3) - 40, (WINDOW_HEIGHT / 3) + 80)
        with open(os.path.join(DIRECTORY, HS_FILE), 'w') as f:
            f.write(str(hs) + '\n')
    lastScore = score
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()

    return score, lastScore, topScore, hs

def game(PLAYERMOVERATE, hs):
    lastScore = 0.0
    topScore = 0.0
    while True:
        # set up the start of the game
        baddies = []
        goodies = []
        powerups = []
        speedups = []
        score = 0.0
        iteration = 0

        playerRect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        musicPlaying = False

        baddieAddCounter = 0
        goodieAddCounter = 0 
        PLAYERMOVERATE = 3 

        while True: # the game loop runs while the game part is playing

            score += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == ord('y'):
                        reverseCheat = True

                    if event.key == ord('x'):
                        slowCheat = True

                    if event.key == K_LEFT or event.key == ord('a'):
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == ord('w'):
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveUp = False
                        moveDown = True

                if event.type == KEYUP:
                    if event.key == ord('y'):
                        reverseCheat = False
                    if event.key == ord('x'):
                        slowCheat = False
                    if event.key == ord('m'):
                        if musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
                    if event.key == K_ESCAPE:
                        terminate()
                    
                        
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

                if event.type == MOUSEMOTION:
                    # If the mouse moves, move the player where the cursor is.
                    playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)


            baddieImage = pygame.image.load(PLAYERS_DIR + 'bad/baddie.png').convert()
            randomBaddieImage = pygame.image.load(random.choice(baddies_list)).convert()
            goodieImage = pygame.image.load(random.choice(goodies_list)).convert()


            # add new baddies
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
                goodieAddCounter += 1

            goodies, baddies, goodieAddCounter, baddieAddCounter, score = checkScore(baddieAddCounter, goodieAddCounter, score, baddies, goodies,
                baddieImage, randomBaddieImage, goodieImage, baddieRates)

            powerups = addNewPowerUpToList(iteration, powerups, powerUpImage)

            speedups = addNewSpeedUpToList(iteration, speedups, speedUpImage)

            # move the player around
            movePlayerAround(moveLeft, moveRight, moveUp, moveDown, playerRect, PLAYERMOVERATE)           

            # move the mouse cursor to match the player.
            pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

            # move baddies down
            score = moveFigureDown(baddies, score, reverseCheat, slowCheat)

            # move goodies down
            score = moveFigureDown(goodies, score, reverseCheat, slowCheat)

            # delete baddies that have fallen past the bottom
            delFigurePastBottom(baddies)

            # delete goodies that have fallen past the bottom
            delFigurePastBottom(goodies)

            # draw the game world on the window
            windowSurface.fill(BACKGROUNDCOLOR)

            # draw scores
            drawText('Score: %s' % (round(score,2)), font, windowSurface, 10, 0)
            drawText('Last: %s' % (round(lastScore, 2)), font, windowSurface, 10, 40)
            drawText('Top Score: %s' % (round(topScore, 2)), font, windowSurface, 10, 80)

            # draw player's rect
            windowSurface.blit(playerImage, playerRect)

            # draw each baddie
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            # draw each baddie
            for g in goodies:
                windowSurface.blit(g['surface'], g['rect'])

            for p in powerups:
                windowSurface.blit(p['surface'], p['rect'])

            for s in speedups:
                windowSurface.blit(s['surface'], s['rect'])

            pygame.display.update()


            # check if any baddies have hit the player
            if playerHasHitBaddie(playerRect, baddies):
                break
                

            if playerHasHitGoodie(playerRect, goodies):
                score = score + 50.0


            if playerHasHitPowerUp(playerRect, powerups):
                score = score + 200.0


            if playerHasHitSpeedUp(playerRect, speedups):
                PLAYERMOVERATE += 1
                playerRect.move_ip(0, PLAYERMOVERATE)

            iteration += 1
            mainClock.tick(FPS)

        # stop the game and show GAME OVER
        score, lastScore, topScore, hs = game_over(score, lastScore, topScore, hs)


def main():
    hs = main_menu()
    game(PLAYERMOVERATE, hs)
            
if __name__ == "__main__":
    main() 