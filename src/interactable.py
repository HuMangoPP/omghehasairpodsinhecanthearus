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
        self.rect = self.image.get_rect(center=(500,500))
    
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
    
    def check_vertical_collision(self):
        self.rect.y+=1
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        self.rect.y-=1
        if colliding_sprites:
            if self.velocity[1]>0:
                self.rect.bottom=colliding_sprites[0].rect.top
            elif self.velocity[1]<0:
                self.rect.top=colliding_sprites[0].rect.bottom
            self.velocity[1] = 0

    def check_horizontal_collision(self):
        self.rect.y-=1
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        self.rect.y+=1
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
            self.rect.x=self.player.rect.x
            self.rect.y=self.player.rect.y-TILESIZE
        else:
            self.fall()