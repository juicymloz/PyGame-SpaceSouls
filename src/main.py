import pygame, random, os,time, sys
from mobs import *
from animations import Shot
from button import *

pygame.mixer.init()
pygame.init()
pygame.display.set_caption('SS')

heigthScreen,widthScreen = 800,1200
screen = pygame.display.set_mode((widthScreen,heigthScreen))
clock = pygame.time.Clock()
player=Player('imgs/spaceship.png')
bg = pygame.image.load('imgs/bg1.png')
playerGroup = pygame.sprite.Group()
bossGroup = pygame.sprite.Group()
shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
soundShoot = pygame.mixer.Sound('sounds/shot.mp3')
soundShoot.set_volume(0.2)
soundTrack = pygame.mixer.Sound("sounds/soundtrack1.mp3")

enemieHeight = 80
widthProportion = widthScreen / 10
heightProportion = heigthScreen / 12
level = 1
scroll = 0

hordes_by_level = []
boss_object = None

def loadEnemies(which_level):
    global hordes_by_level, boss_object
    hordes_by_level = []
    nw_horde = []
    if which_level == 1:
        path = "src/hordeslvl1.txt"
    elif which_level == 2:
        path = "src/hordeslvl2.txt"
    elif which_level == 3:
        path = "src/hordeslvl3.txt"
    with open(path) as f:
        if which_level == 3:
            boss = f.readline().strip().split(',')
            boss_object = Enemie1(eval(boss[0]), eval(boss[1]), int(boss[2]), int(boss[3]), int(boss[4]))
        enemies_per_horde = [int(x) for x in next(f).split(",")]
        for x in enemies_per_horde:
            for y in range(x):
                enemie = f.readline().strip().split(',')
                print(enemie)
                enemie_object = Enemie1(eval(enemie[0]), eval(enemie[1]), int(enemie[2]), int(enemie[3]), int(enemie[4]))
                nw_horde.append(enemie_object)
            hordes_by_level.append(nw_horde)
            nw_horde = []
            print(hordes_by_level)

stars = []

for i in range(50):
    x=random.randrange(0,widthScreen)
    y=random.randrange(0,heigthScreen)
    radious = random.randrange(1,3)
    stars.append([x,y,radious])

def scrollingBackground(scroll):
    global bg
    rect = bg.get_rect()
    for i in range(2):
        screen.blit(bg,(i*rect.width+scroll,heigthScreen-rect.height))
    scroll-=1
    if scroll<-1200:
        scroll=0
    return scroll

def drawStars(stars):
    for i in range(len(stars)):
        pygame.draw.circle(screen,(255,255,255),(stars[i][0],stars[i][1]),stars[i][2])
        stars[i][0]-=1
        if stars[i][0]+stars[i][2]<0:
            stars[i][0]=widthScreen+stars[i][2]
            stars[i][1]-=5
            if stars[i][1]+stars[i][2]<0:
                stars[i][1]=heigthScreen+stars[i][2]

def shoot(type,spaceship,start,firerate):
        global shots

        if spaceship.boss:
            x = spaceship.rect.left
            y = spaceship.rect.top
        else:
            if type == 1:
                x = spaceship.rect.right
                y = spaceship.rect.centery-10
            elif type==2:
                x = spaceship.rect.left
                y = spaceship.rect.centery-10
    
        interval = time.time()
        
        if interval-start>firerate:
            soundShoot.play()
            if spaceship.boss:
                shot4 = Shot(x,y,type)
                shot2 = Shot(x,y+150,type)
                shot3 = Shot(x,y+310,type)
                shots.add([shot2,shot3,shot4])
            else:
                shot1 = Shot(x,y,type)
                shots.add(shot1)
            return interval
        else:
            return start
        
def drawLifeLine():
    color = ()
    if player.health < 70:
        color = (254,45,1)
    elif player.health < 120:
        color = (254,101,1)
    else:
        color = (24,254,1)
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(1070,30,104,30),2)
    if player.health>0:
        pygame.draw.line(screen,color,(1072,44),(1072+player.health/2,44),26)

def drawPoints():
    points_text = get_font(30,'assets/OptimusPrinceps.ttf').render("score : "+str(player.score), True, "#FFFFFF")
    points_rect = points_text.get_rect(center=(980, 45))
    screen.blit(points_text, points_rect)

def gameOver():
    global level
    running = True
    """SMILE DOG JIJI"""
    xd = pygame.image.load('imgs/smiledog.jpg')
    screen.blit(xd,(0,0))
    jeffisound = pygame.mixer.Sound("sounds/jeff.mp3")
    pygame.mixer.Sound.play(jeffisound,-1).set_volume(0.5)
    """SMILE DOG JIJI"""
    while running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        gameover_text = get_font(120,'assets/OptimusPrinceps.ttf').render("GAME OVER", True, "#fa0505")
        gameover_rect = gameover_text.get_rect(center=(widthScreen/2, heigthScreen/2))
        screen.blit(gameover_text, gameover_rect)
        QUIT_BUTTON = Button(None,pos=(widthScreen/2, 520), 
                                text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="#f5310a")
        
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound.stop(jeffisound)
                    level = 1
                    player.score = 0
                    player.health = 200
                    running = False
        pygame.display.update()

def get_font(size,font="assets/halflife.ttf"): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(font, size)

def menuInGame():
    global level, soundTrack, levelEnemy
    running = True
    while running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        buttons = []
        if level<4:
            CONTINUE_BUTTON = Button(None, pos=(widthScreen/2, 300), 
                                text_input="CONTINUE", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
            SAVE_BUTTON = Button( None,pos=(widthScreen/2, 400), 
                                text_input="SAVE", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
            buttons = [CONTINUE_BUTTON, SAVE_BUTTON]
        else:
            score_text = get_font(50,'assets/OptimusPrinceps.ttf').render("score : "+str(player.score), True, "#FFFFFF")
            score_rect = score_text.get_rect(center=(widthScreen/2, 350))
            screen.blit(score_text, score_rect)
            
        QUIT_BUTTON = Button(None,pos=(widthScreen/2, 500), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
        buttons.append(QUIT_BUTTON)    

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if level < 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        resetPlayer()
                        loadEnemies(level)
                        change_level(level)
                        play()
                    if SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        saveGame()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        soundTrack.stop()
                        resetPlayer()
                        level = 1
                        player.score = 0
                        player.health = 200
                        running = False                 
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        running = False

        pygame.display.update()

def drawGame():
    global scroll, clock

    screen.fill((0,0,0))
    drawStars(stars)
    drawLifeLine()
    drawPoints()
    scroll = scrollingBackground(scroll)
    playerGroup.draw(screen)
    bossGroup.draw(screen)
    enemies.draw(screen)
    shots.draw(screen)
    clock.tick(60)
    pygame.display.update()

def saveGame():
    global scroll
    with open('savestate.txt', 'w') as f:
        f.write(str(level)+"\n")
        f.write(str(player.score)+"\n")
        f.write(str(player.health))
    saved_text = get_font(50,'assets/OptimusPrinceps.ttf').render("Game Saved", True, "#fa0505")
    saved_rect = saved_text.get_rect(center=(widthScreen/2, 200))
    screen.blit(saved_text, saved_rect)
    start = time.time()
    stop = time.time()
    while stop-start<1:
        stop = time.time()
        pygame.display.update()
    drawGame()
        
def loadGame():
    global level,player

    text = ""
    try:
        with open('savestate.txt') as f:
            level = int(f.readline().strip())
            player.score = int(f.readline().strip())
            player.health = int(f.readline().strip())
            text = "Game Loaded"
    except:
        text = "No saved game founded"
    loaded_text = get_font(50,'assets/OptimusPrinceps.ttf').render(text, True, "#fa0505")
    loaded_rect = loaded_text.get_rect(center=(widthScreen/2, 300))
    start = time.time()
    stop = time.time()
    while stop-start<1:
        stop = time.time()
        main_menu()
        screen.blit(loaded_text, loaded_rect)
        pygame.display.update()
    if text == "Game Loaded":
        resetPlayer()
        loadEnemies(level)
        change_level(level)
        play()

def change_level(level):
    global bg, player, soundTrack
    if level == 1:
        bg = pygame.image.load('imgs/bg1.png')
        soundTrack.stop()
        soundTrack = pygame.mixer.Sound("sounds/soundtrack1.mp3")
    elif level == 2:
        bg = pygame.image.load('imgs/bg2.png')
        soundTrack.stop()
        soundTrack = pygame.mixer.Sound("sounds/soundtrack2.mp3")
    elif level == 3:
        bg = pygame.image.load('imgs/bg3.png')
        soundTrack.stop()
        soundTrack = pygame.mixer.Sound("sounds/soundtrack2.mp3")
        bossGroup.add(boss_object)
    
def resetPlayer():
    global player, playerGroup
    if len(playerGroup)==0:
        playerGroup.add(player)
        player.image = player.imageSpaceShip
    enemies.empty()
    shots.empty()
    bossGroup.empty()
    player.rect.x = 0
    player.rect.y = 0
    player.velX = 0
    player.velY = 0

def main_menu():
    soundTrack.stop()
    screen.fill((0,0,0))
    drawStars(stars)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    GAME_TEXT = get_font(90).render("S P a C E - S O U L S", True, "#f07c00")
    GAME_RECT = GAME_TEXT.get_rect(center=(widthScreen/2, 200))

    PLAY_BUTTON = Button(None, pos=(widthScreen/2, 400), 
                        text_input="NEW GaME", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
    LOAD_BUTTON = Button( None,pos=(widthScreen/2, 500), 
                        text_input="LOaD", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
    CREDITS_BUTTON = Button( None,pos=(widthScreen/2, 600), 
                        text_input="CREDITS", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")
    QUIT_BUTTON = Button(None,pos=(widthScreen/2, 700), 
                        text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="#f5310a")

    screen.blit(GAME_TEXT, GAME_RECT)

    for button in [PLAY_BUTTON, LOAD_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                resetPlayer()
                change_level(level)
                loadEnemies(level)
                play()
            if LOAD_BUTTON.checkForInput(MENU_MOUSE_POS):
                loadGame()
            if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                credits()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

def credits():
    running = True
    while running:
        screen.fill((0,0,0))
        drawStars(stars)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        credits_text = get_font(40,'assets/OptimusPrinceps.ttf').render("Design and developed by", True, "#f5c30a")
        javier = get_font(35,'assets/OptimusPrinceps.ttf').render("Javier Bernabe Garcia", True, "#f5c30a")
        juan = get_font(35,'assets/OptimusPrinceps.ttf').render("Juan Carlos Maldonado Lozano", True, "#f5c30a")
        fredo = get_font(35,'assets/OptimusPrinceps.ttf').render("Alfredo Cordoba Rios", True, "#f5c30a")
        arranged_text = get_font(40,'assets/OptimusPrinceps.ttf').render("Music composed, arranged and produced by", True, "#f5c30a")
        erick = get_font(35,'assets/OptimusPrinceps.ttf').render("Erick Ramon Ortega", True, "#f5c30a")
        QUIT_BUTTON = Button(None,pos=(1100, 720), 
                            text_input="BaCK", font=get_font(40), base_color="#d7fcd4", hovering_color="#f5310a")
        
        credits_rect = credits_text.get_rect(center=(widthScreen/2, 150))
        javier_rect = javier.get_rect(center = (widthScreen/2,250))
        juan_rect = juan.get_rect(center=(widthScreen/2,300))
        fredo_rect = fredo.get_rect(center=(widthScreen/2,350))
        arranged_rect = arranged_text.get_rect(center=(widthScreen/2,450))
        erick_rect = erick.get_rect(center=(widthScreen/2,600))

        screen.blit(credits_text, credits_rect)
        screen.blit(javier, javier_rect)
        screen.blit(juan, juan_rect)
        screen.blit(fredo,fredo_rect)
        screen.blit(arranged_text,arranged_rect)
        javier_rect.centery = 550
        screen.blit(javier, javier_rect)
        screen.blit(erick, erick_rect)

        for button in [ QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False

        pygame.display.update()

def play():
    global level, soundTrack
    soundTrack.play(-1).set_volume(0.5)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                soundTrack.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (len(enemies)>0 or len(bossGroup)>0):
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.velX=-5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.velX=5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.velY=-5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.velY=5
                if event.key == pygame.K_j and len(playerGroup)>0:
                    player.shooting = True
                    player.interval = time.time()

            if event.type == pygame.KEYUP and (len(enemies)>0 or len(bossGroup)>0):
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velX=0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velY=0
                if event.key == pygame.K_j:
                    player.shooting = False

        if player.shooting==True:
            player.interval=shoot(1,player,player.interval,0.4)

        enemiesList = enemies.sprites()
        if level == 3:
            randomhorde = 0#random.randint(0,1)
            if len(enemies) == 0 and len(hordes_by_level)>0 and len(bossGroup)>0:
                print(hordes_by_level[randomhorde][0].rect.x)
                for i in range(3):
                    hordes_by_level[randomhorde][i].rect.x = random.randint(widthScreen, widthScreen + widthProportion * 3)
                    hordes_by_level[randomhorde][i].rect.y = random.randint(0, heigthScreen - enemieHeight)
                    hordes_by_level[randomhorde][i].spriteNumber = 0
                    hordes_by_level[randomhorde][i].death = False
                    hordes_by_level[randomhorde][i].health = 200
                    hordes_by_level[randomhorde][i].image = hordes_by_level[randomhorde][i].imageSpaceShip
                    if i == 0:
                        print(hordes_by_level[randomhorde][i].rect.x)
                enemies.add(hordes_by_level[randomhorde])
            if len(bossGroup)==0 and len(enemiesList)>0:
                for x in enemiesList:
                    x.death = True
                shots.empty()
        else:
            if len(enemiesList) == 0 and len(hordes_by_level)>0:
                enemies.add(hordes_by_level.pop(0))
            
        if len(enemies)==0 and len(bossGroup)==0:
            player.shooting = False
            player.levelComplete = True
            player.velX = 4
            player.velY = -2
            if player.rect.left>1300:
                running = False

        for enemie in enemiesList:
            if enemie.shooting==True:
                enemie.interval = shoot(2,enemie,enemie.interval,1.5)
        if len(bossGroup)>0 and boss_object.shooting:
            boss_object.interval = shoot(2,boss_object,boss_object.interval,1)

        if len(playerGroup)==0:
            running = False

        #print(shots)
        enemies.update(shots,player)
        playerGroup.update(shots,player)
        bossGroup.update(shots,player)
        shots.update()

        drawGame()
    
    if player.levelComplete:
        level += 1
        menuInGame()
    else:
        soundTrack.stop()
        gameOver()

while True:
    main_menu()
    pygame.display.update()