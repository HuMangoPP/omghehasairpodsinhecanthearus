import pygame
from src.settings import *

class Interactable(pygame.sprite.Sprite):
    def __init__(self,groups, type,obstacle_sprites,player):
        super().__init__(groups)
        self.type = type
        self.picked_up = False
        self.velocity = [0,0]
        self.gravity=0.5
        self.friction = 0.2
        self.obstacle_sprites=obstacle_sprites
        self.player=player
    
    def import_img(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(center=(300,500))
        self.pickup_box = self.rect.inflate(TILESIZE,TILESIZE)
    
    def fall(self):
        self.velocity[1]+=self.gravity

    def slow_down(self):
        if self.velocity[0]>self.friction:
            self.velocity[0]-=self.friction
        elif self.velocity[0]<-self.friction:
            self.velocity[0]+=self.friction
        else:
            self.velocity[0]=0

    def move(self):
        self.rect.x+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.y+=self.velocity[1]
        self.check_vertical_collision()
        self.pickup_box.center = self.rect.center
    
    def check_vertical_collision(self):
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        if colliding_sprites:
            if self.velocity[1]>0:
                self.rect.bottom=colliding_sprites[0].rect.top
            elif self.velocity[1]<0:
                self.rect.top=colliding_sprites[0].rect.bottom
            self.velocity[1] = 0

    def check_horizontal_collision(self):
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        if colliding_sprites:
            if self.velocity[0]>0:
                self.rect.right=colliding_sprites[0].rect.left
            elif self.velocity[0]<0:
                self.rect.left=colliding_sprites[0].rect.right
            self.velocity[0]=0

    def update(self):
        self.slow_down()
        self.move()
        if self.picked_up:
            if self.player.facing=='right':
                self.rect.left = self.player.rect.right
            else:
                self.rect.right = self.player.rect.left
            self.rect.bottom = self.player.rect.bottom
        else:
            self.fall()