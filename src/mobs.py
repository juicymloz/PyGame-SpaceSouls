import pygame, time
from animations import *
from random import uniform

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,route,width,height, health, x=0,y=0):
        super().__init__()
        self.imageOrigin = pygame.image.load(route).convert_alpha()
        self.imageSpaceShip = pygame.transform.scale(self.imageOrigin,[width,height])
        self.image = self.imageSpaceShip
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.velX=0
        self.velY=0
        self.shooting = False
        self.widthScreen = 1200
        self.heightScreen = 800
        self.interval=time.time()
        self.health = health
        self.death = False
        self.spriteNumber = 0
        self.score = 0
        self.soundDamage = None
        self.soundDestroy = None
        self.crash = Crash()
        self.player = False
        self.bulletType = 0
        self.boss = False
    
    def update(self, bullets, player):
        for shot in bullets:
            if pygame.sprite.collide_rect(self, shot) and shot.type != self.bulletType:
                shot.kill()
                self.health -= shot.damage
                self.soundDamage.play()
                if self.bulletType == 2:
                    player.score += 20

        if self.health <= 0:
            self.death = True
            if not self.player and self.spriteNumber == 0:
                player.score+=50

        if self.death == True:
            if self.spriteNumber == 0:
                self.soundDestroy.play()
            self.image = pygame.transform.scale(self.crash.sprites[int(self.spriteNumber)],[self.rect.width,self.rect.height])
            self.spriteNumber+=1
        
        if self.spriteNumber>=48:
            self.kill()

class Player(Spaceship):
    def __init__(self,route: str):
        super().__init__(route,90,70,200)
        self.soundDamage = pygame.mixer.Sound('sounds/damage1.mp3')
        self.soundDamage.set_volume(0.2)
        self.soundDestroy = pygame.mixer.Sound('sounds/crash1.mp3')
        self.soundDestroy.set_volume(0.2)
        self.levelComplete = False
        self.player = True
        self.bulletType = 1
        
    def update(self,bullets,player):
        super().update(bullets,player)
        if self.rect.x + self.rect.width > self.widthScreen and self.levelComplete == False:
            self.rect.x=self.widthScreen-self.rect.width
        elif self.rect.x<0:
            self.rect.x=0
        self.rect.x += self.velX
        
        if self.rect.y>self.heightScreen-self.rect.height:
            self.rect.y=self.heightScreen-self.rect.height
        elif self.rect.y<0:
            self.rect.y=0
        self.rect.y += self.velY


class Enemie1(Spaceship):
    def __init__(self,x,y,movement, startpos, type) -> None:
        health = 100
        height, width = 80, 80
        if type == 1:
            route='imgs\spaceship_enemie1.png'
        elif type == 2:
            route='imgs\spaceship_enemie2.png'
        elif type == 3:
            route='imgs\spaceship_enemie3.png'
        elif type == 4:
            route='imgs\spaceship_boss1.png'
            health = 5000
            height, width = 320, 320
        super().__init__(route,width,height,health,x,y)
        self.velX=1
        self.velY=1
        self.movement = movement
        self.startpos = startpos
        self.direction = 1
        if self.movement == 6:
            self.boss = True
        self.soundDamage = pygame.mixer.Sound('sounds/damage2.mp3')
        self.soundDamage.set_volume(0.3)
        self.soundDestroy = pygame.mixer.Sound('sounds/crash2.mp3')
        self.soundDestroy.set_volume(0.3)
        self.bulletType = 2

    def update(self, bullets, player):
        super().update(bullets, player)
        if not self.shooting and self.rect.left<self.widthScreen and self.rect.bottom<self.heightScreen and self.rect.top>0:
            self.shooting = True
            if self.movement!=6:
                self.interval = time.time()+uniform(0,0.5)
        if self.movement == 1:
            self.rect.x-=self.velX * 2
        elif self.movement == 2:
            self.rect.x -= self.velX
            self.rect.y += self.velY
        elif self.movement == 3:
            self.rect.x += self.velX
            self.rect.y += self.velY
        elif self.movement == 4:
            self.rect.x += self.velX
            self.rect.y -= self.velY
        elif self.movement == 5:
            self.rect.x -= self.velX * 2
            self.rect.y -= self.velY
        elif self.movement == 6:
            if self.direction == 1:
                if self.rect.left > (self.widthScreen/10 * 7):
                    self.rect.x -= self.velX * 2
                else:
                    self.direction = 2
                    self.velX *= -1
            else:
                if self.rect.left <= (self.widthScreen/10 * 7) or self.rect.right >= self.widthScreen:
                    self.velX *= -1
                if self.rect.top <= 0 or self.rect.bottom >= self.heightScreen:
                    self.velY *= -1
                self.rect.x += self.velX * 2
                self.rect.y += self.velY
            
        if self.startpos == 1 and (self.rect.right <= 0 or self.rect.top > self.heightScreen):
            self.kill()
        if self.rect.bottom < 0 and self.startpos == 2:
            self.kill()

