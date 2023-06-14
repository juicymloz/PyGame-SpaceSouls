import pygame

class Crash():
    def __init__(self, route='imgs/crash.png') -> None:
        self.imageOrigin = pygame.image.load(route).convert_alpha()
        self.rect = self.imageOrigin.get_rect()
        width = self.rect.width/8
        height = self.rect.height/6
        self.sprites = []
        for i in range(6):
            for j in range(8):
                n_rec = pygame.Rect((j * width ,i*height,width,height))
                self.sprites.append(self.imageOrigin.subsurface(n_rec))


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        if type == 1:
            self.damage = 50
            self.velX = 5
            route = 'imgs/laserBullet.png'
        elif type==2:
            self.damage = 20
            self.velX = -5
            route = 'imgs/bullet_enemie.png'
        self.type=type
        self.image = pygame.image.load(route).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        super().update()
        if self.rect.left>1200 or self.rect.right<0:
            self.kill()
        else:
            self.rect.x+=self.velX