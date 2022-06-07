import pygame
from src.settings import *

class Character(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites,interactable_sprites):
        super().__init__(groups)
        # movement logic
        self.speed = 3
        self.velocity = [self.speed, 0]
        self.acc = 0.4
        self.gravity = 0.5
        self.falling = [True, True]
        self.facing = 'right'

        # data
        self.deaths = 0
        self.boing = pygame.mixer.Sound('./sounds/boing.wav')
        
        # collision logic
        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites = interactable_sprites
        self.sprung = False
        self.sprung_cd = 100
        self.sprung_time = None

    def import_img(self, img):
        self.assets = img
        self.image = self.assets[self.facing][0]
        self.rect = self.image.get_rect(center=(100,21*TILESIZE))

    def check_interactable_collision(self):
        interacting_sprites = pygame.sprite.spritecollide(self,self.interactable_sprites,False)
        if interacting_sprites and not self.sprung:
            spring = interacting_sprites[0]
            if not spring.picked_up:
                self.boing.play()
                self.sprung = True
                self.sprung_time = pygame.time.get_ticks()
                if spring.orientation == 'vertical':
                    self.velocity[1] = -spring.vertical_spring
                else:
                    if spring.rect.centerx<=self.rect.centerx:
                        self.velocity[0] = spring.horizontal_spring
                    else:
                        self.velocity[0] = -spring.horizontal_spring

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
            if not self.falling[0] or not self.falling[1]:
                self.velocity[0]=-self.velocity[0]

    def check_death(self,current_level):
        if self.rect.y>=HEIGHT+200:
            self.reset()
            if current_level!=0:
                self.deaths+=1

    def reset(self):
        self.rect.center = (100,21*TILESIZE)

    def check_goal(self):
        if self.rect.x>=WIDTH+TILESIZE:
            return True

    def fall(self):
        if self.falling[0] or self.falling[1]:
            self.velocity[1]+=self.gravity

    def move(self):
        if self.velocity[0]>0:
            self.facing = 'right'
        else:
            self.facing = 'left'
        self.rect.x+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.y+=self.velocity[1]
        self.check_vertical_collision()

        if self.velocity[0]>self.speed+self.acc:
            self.velocity[0]-=self.acc
        elif self.velocity[0]<-self.speed-self.acc:
            self.velocity[0]+=self.acc

    def check_cd(self):
        time = pygame.time.get_ticks()
        if self.sprung:
            if time-self.sprung_time>self.sprung_cd:
                self.sprung = False

    def animate(self):
        self.image = self.assets[self.facing][0]

    def update(self,current_level):
        self.check_cd()
        self.check_death(current_level)
        self.fall()
        self.check_interactable_collision()
        self.move()
        self.animate()