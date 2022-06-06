import pygame
from src.settings import *

class Interactable(pygame.sprite.Sprite):
    def __init__(self,groups, type,obstacle_sprites,player):
        super().__init__(groups)
        # type of interactable currently only spring exists
        self.type = type

        # movement logic
        self.picked_up = True
        self.velocity = [0,0]
        self.gravity=0.5
        self.friction = 0.2

        # collision logic
        self.obstacle_sprites=obstacle_sprites
        self.player=player
        self.player.holding_item=self

        # data
        self.deaths = 0
    
    def import_img(self, img):
        self.assets = img
        self.image = self.assets[self.type][0]
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
        rightmost = None
        leftmost = None
        for sprite in colliding_sprites:
            if rightmost == None:
                rightmost = sprite.rect.right
            else:
                rightmost = max(sprite.rect.right,rightmost)
            if leftmost == None:
                leftmost = sprite.rect.left
            else:
                leftmost = min(sprite.rect.left,leftmost)
            
        if colliding_sprites:
            if self.velocity[0]>0:
                self.rect.right=leftmost
            elif self.velocity[0]<0:
                self.rect.left=rightmost
            self.velocity[0]=0

    def check_death(self,current_level):
        if self.rect.y>=HEIGHT+200:
            self.reset()
            if current_level!=0:
                self.deaths+=1

    def reset(self):
        self.player.holding_item = self
        self.picked_up = True
        self.velocity = [0,0]

    def update(self,current_level):
        self.check_death(current_level)
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