import pygame

from src.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites,interactable_sprites):
        super().__init__(groups)
        # movement logic 
        self.velocity = [0, 0]
        self.speed = 3
        self.acc = 0.4
        self.jump_speed = 12
        self.jumps = 1
        self.gravity = 0.5
        self.falling = [True, True]
        self.holding_item = None
        self.facing = 'right'
        self.throw_speed = 8

        # data
        self.deaths = 0

        # collision logic
        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites=interactable_sprites

    def import_img(self, img):
        self.assets = img
        self.image = self.assets[self.facing][0]
        self.rect = self.image.get_rect(center=(100,21*TILESIZE))
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.facing = 'right'
            if self.velocity[0]<self.speed:
                self.velocity[0]+=self.acc
            else:
                self.velocity[0]=self.speed
        elif keys[pygame.K_a]:
            self.facing = 'left'
            if self.velocity[0]>-self.speed:
                self.velocity[0]-=self.acc
            else:
                self.velocity[0]=-self.speed
        else:
            if self.velocity[0]>self.acc:
                self.velocity[0]-=self.acc
            elif self.velocity[0]<-self.acc:
                self.velocity[0]+=self.acc
            else:
                self.velocity[0] = 0

    def check_vertical_collision(self):
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        if colliding_sprites:
            if self.velocity[1]>0:
                self.rect.bottom=colliding_sprites[0].rect.top
                self.falling = [self.falling[1], False]
            elif self.velocity[1]<0:
                self.rect.top=colliding_sprites[0].rect.bottom
                self.falling = [self.falling[1], True]
            self.velocity[1] = 0
            self.jumps = 1
        else:
            self.falling = [self.falling[1], True]

    def check_horizontal_collision(self):
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        if colliding_sprites:
            if self.velocity[0]>0:
                self.rect.right=colliding_sprites[0].rect.left
            elif self.velocity[0]<0:
                self.rect.left=colliding_sprites[0].rect.right
            self.velocity[0]=0

    def fall(self):
        if self.falling[0] or self.falling[1]:
            self.velocity[1]+=self.gravity

    def pickup_interactable(self):
        for sprite in self.interactable_sprites:
            if self.rect.colliderect(sprite.pickup_box) and self.holding_item==None:
                sprite.picked_up=True
                self.holding_item=sprite

    def throw_interactable(self):
        if self.facing=='right':
            self.holding_item.velocity[0]=self.velocity[0]/2+self.throw_speed
        else:
            self.holding_item.velocity[0]=self.velocity[0]/2-self.throw_speed
        self.holding_item.picked_up=False
        self.holding_item = None

    def check_death(self,current_level):
        if self.rect.centery>=HEIGHT+200:
            self.reset()
            if current_level!=0:
                self.deaths+=1

    def reset(self):
        self.rect.center = (100,21*TILESIZE)

    def move(self):
        self.rect.centerx+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.centery+=self.velocity[1]
        self.check_vertical_collision()

    def animate(self):
        self.image = self.assets[self.facing][0]

    def update(self,current_level):
        self.check_death(current_level)
        self.input()
        self.fall()
        self.move()
        self.animate()