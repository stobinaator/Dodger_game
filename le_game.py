import pygame, random, sys
from pygame.locals import *



WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8

baddieRates = {'one' : {'ADDNEWBADDIERATE1':15,'ADDNEWGOODIERATE1':24}, # until 500
               'two' : {'ADDNEWBADDIERATE2':13,'ADDNEWGOODIERATE2':26}, # above 500
               'three' : {'ADDNEWBADDIERATE3':11,'ADDNEWGOODIERATE3':28}, # above 1500
               'four' : {'ADDNEWBADDIERATE4':9,'ADDNEWGOODIERATE4':30}, # above 3000
               'five' : {'ADDNEWBADDIERATE5':7,'ADDNEWGOODIERATE5':32}, # above 5000
               'six' : {'ADDNEWBADDIERATE6':5,'ADDNEWGOODIERATE6':32}, # above 7000
               'seven' : {'ADDNEWBADDIERATE7':6,'ADDNEWGOODIERATE7':32}, # above 10k
               }

PLAYERMOVERATE = 5


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
                    terminate()
                return


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
    for b in whoever[:]:
        if b['rect'].top > WINDOW_HEIGHT:
            whoever.remove(b)


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



# set up game, the window, the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 48)


# sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('bird.mp3')

# images
baddies_list = ['radichat.png', 'danko.png', 'bocko.png', 'anne.png',
                'ceci.png', 'regi.png', 'lazo.png', 'aleko.png']
baddies_list = ['players/bad/'+b for b in baddies_list]
goodies_list = ['players/good/stobko.png', 'players/good/shosho.png']
playerImage = pygame.image.load('players/player.png')
playerRect = playerImage.get_rect()


# start screen
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOW_WIDTH/3) + 30, (WINDOW_HEIGHT/3))


pygame.display.update()
waitForPlayerToPressKey()

windowSurface.fill(BACKGROUNDCOLOR)
drawText('There are 7 stages',
         font, windowSurface, 110, (WINDOW_HEIGHT/3))
drawText('Use arrows or wasd',
         font, windowSurface, 110, (WINDOW_HEIGHT/3) + 50)
drawText('X to slow down time',
         font, windowSurface, 110, (WINDOW_HEIGHT/3) + 100)
drawText('Y to make them fly backwards',
         font, windowSurface, 110, (WINDOW_HEIGHT/3) + 150)
drawText('Press a key to start', font, windowSurface, 110,
                                                     (WINDOW_HEIGHT/3) + 200)
pygame.display.update()
waitForPlayerToPressKey()

def main():
    lastScore = 0.0
    topScore = 0.0
    while True:
        # set up the start of the game
        baddies = []
        goodies = []
        score = 0.0

        playerRect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        musicPlaying = True



        baddieAddCounter = 0
        goodieAddCounter = 0
        pygame.mixer.music.play(-1, 0.0)

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


            baddieImageUntil500 = pygame.image.load('players/bad/baddie.png')
            randomImageUntil1500 = pygame.image.load(random.choice(baddies_list[:2]))
            randomImageUntil3000 = pygame.image.load(random.choice(baddies_list[2:4]))
            randomImageUntil5000 = pygame.image.load(random.choice(baddies_list[4:6]))
            randomImageUntil7000 = pygame.image.load(random.choice(baddies_list[6:]))
            randomBaddieImage = pygame.image.load(random.choice(baddies_list))
            goodieImage = pygame.image.load(random.choice(goodies_list))


            # add new baddies
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
                goodieAddCounter += 1

            if score > 10000:
                if baddieAddCounter >= baddieRates['seven']['ADDNEWBADDIERATE7']:
                    baddieAddCounter = baddieRates['seven']['ADDNEWBADDIERATE7']
                    if baddieAddCounter == baddieRates['seven']['ADDNEWBADDIERATE7']:
                        # print('SEVENTH 5')
                        baddieAddCounter = 0
                        newBaddie = addNewFigure(randomBaddieImage)
                        baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['seven']['ADDNEWGOODIERATE7']:
                    goodieAddCounter = baddieRates['seven']['ADDNEWGOODIERATE7']
                    if goodieAddCounter == baddieRates['seven']['ADDNEWGOODIERATE7']:
                        # print('SEVENTH 32')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score > 7000:
                if baddieAddCounter >= baddieRates['six']['ADDNEWBADDIERATE6']:
                    baddieAddCounter = baddieRates['six']['ADDNEWBADDIERATE6']
                    if baddieAddCounter == baddieRates['six']['ADDNEWBADDIERATE6']:
                        # print('SIXTH 6')
                        baddieAddCounter = 0
                        newBaddie = addNewFigure(randomBaddieImage)
                        baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['six']['ADDNEWGOODIERATE6']:
                    goodieAddCounter = baddieRates['six']['ADDNEWGOODIERATE6']
                    if goodieAddCounter == baddieRates['six']['ADDNEWGOODIERATE6']:
                        # print('SIXTH 32')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score > 5000:
                if baddieAddCounter >= baddieRates['five']['ADDNEWBADDIERATE5']:
                    baddieAddCounter = baddieRates['five']['ADDNEWBADDIERATE5']
                    if baddieAddCounter == baddieRates['five']['ADDNEWBADDIERATE5']:
                        # print('FIFTH 7')
                        baddieAddCounter = 0
                        newBaddie = addNewFigure(randomImageUntil7000)
                        baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['five']['ADDNEWGOODIERATE5']:
                    goodieAddCounter = baddieRates['five']['ADDNEWGOODIERATE5']
                    if goodieAddCounter == baddieRates['five']['ADDNEWGOODIERATE5']:
                        # print('FIFTH 32')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score > 3000:
                if baddieAddCounter >=  baddieRates['four']['ADDNEWBADDIERATE4']:
                    baddieAddCounter = baddieRates['four']['ADDNEWBADDIERATE4']
                    if baddieAddCounter == baddieRates['four']['ADDNEWBADDIERATE4']:
                        # print('FOURTH 9')
                        baddieAddCounter = 0
                        newBaddie = addNewFigure(randomImageUntil5000)
                        baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['four']['ADDNEWGOODIERATE4']:
                    goodieAddCounter = baddieRates['four']['ADDNEWGOODIERATE4']
                    if goodieAddCounter == baddieRates['four']['ADDNEWGOODIERATE4']:
                        # print('FOURTH 30')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score > 1500:
                if baddieAddCounter >= baddieRates['three']['ADDNEWBADDIERATE3']:
                    baddieAddCounter = baddieRates['three']['ADDNEWBADDIERATE3']
                    if baddieAddCounter == baddieRates['three']['ADDNEWBADDIERATE3']:
                        # print('THIRD 11')
                        baddieAddCounter = 0
                        newBaddie = addNewFigure(randomImageUntil3000)
                        baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['three']['ADDNEWGOODIERATE3']:
                    goodieAddCounter = baddieRates['three']['ADDNEWGOODIERATE3']
                    if goodieAddCounter == baddieRates['three']['ADDNEWGOODIERATE3']:
                        # print('THIRD 28')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score > 500:
                if baddieAddCounter >= baddieRates['two']['ADDNEWBADDIERATE2']:
                    baddieAddCounter = baddieRates['two']['ADDNEWBADDIERATE2']
                    if baddieAddCounter == baddieRates['two']['ADDNEWBADDIERATE2']:
                         # print('SECOND 13')
                         baddieAddCounter = 0
                         newBaddie = addNewFigure(randomImageUntil1500)
                         baddies.append(newBaddie)
                if goodieAddCounter >= baddieRates['two']['ADDNEWGOODIERATE2']:
                    goodieAddCounter = baddieRates['two']['ADDNEWGOODIERATE2']
                    if goodieAddCounter == baddieRates['two']['ADDNEWGOODIERATE2']:
                        # print('SECOND 26')
                        goodieAddCounter = 0
                        newGoodie = addNewFigure(goodieImage)
                        goodies.append(newGoodie)

            elif score < 500:
                if baddieAddCounter == baddieRates['one']['ADDNEWBADDIERATE1']:
                    # print('FIRST 15')
                    baddieAddCounter = 0
                    newBaddie = addNewFigure(baddieImageUntil500)
                    baddies.append(newBaddie)

                if goodieAddCounter == baddieRates['one']['ADDNEWGOODIERATE1']:
                    # print('FIRST 24')
                    goodieAddCounter = 0
                    newGoodie = addNewFigure(goodieImage)
                    goodies.append(newGoodie)


            # move the player around
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOW_WIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOW_HEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

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

            pygame.display.update()


            # check if any baddies have hit the player
            if playerHasHitBaddie(playerRect, baddies):
                if score > topScore:
                    topScore = score
                lastScore = score
                break


            if playerHasHitGoodie(playerRect, goodies):
                score = score + 50.0


            mainClock.tick(FPS)

        # stop the game and show GAME OVER
        pygame.mixer.music.stop()
        gameOverSound.play()

        drawText('GAME OVER', font, windowSurface, (WINDOW_WIDTH /3),
                                                 (WINDOW_HEIGHT / 3))
        drawText(f'Score: {round(score,2)}', font, windowSurface,
                 (WINDOW_WIDTH / 3) + 20, (WINDOW_HEIGHT / 3) + 40)
        drawText('Press a key to play again.', font, windowSurface,
                 (WINDOW_WIDTH / 3) - 80, (WINDOW_HEIGHT / 3) + 80)
        pygame.display.update()
        waitForPlayerToPressKey()

        gameOverSound.stop()
            
            
if __name__ == "__main__":
    main()           