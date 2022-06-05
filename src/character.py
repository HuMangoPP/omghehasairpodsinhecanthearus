import pygame
from src.settings import *

class Character(pygame.sprite.Sprite):
    def __init__(self, character_type, groups, obstacle_sprites,interactable_sprites):
        super().__init__(groups)
        self.character_type = character_type
        self.speed = 3
        self.velocity = [self.speed, 0]
        self.acc = 0.4
        self.jump_speed = 12
        self.jumps = 1
        self.gravity = 0.5
        self.falling = [True, True]

        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites = interactable_sprites

    def import_img(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect(center=(96,600))

    def check_interactable_collision(self):
        interacting_sprites = pygame.sprite.spritecollide(self,self.interactable_sprites,False)
        for sprite in interacting_sprites:
            if sprite.type == 'spring' and self.velocity[1]>=0 and not sprite.picked_up:
                self.velocity[1]-=self.jump_speed

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

    def check_death(self):
        if self.rect.y>=HEIGHT+200:
            self.rect.center = (96,600)

    def fall(self):
        if self.falling[0] or self.falling[1]:
            self.velocity[1]+=self.gravity

    def move(self):
        self.rect.x+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.y+=self.velocity[1]
        self.check_vertical_collision()

    def update(self):
        self.check_death()
        self.fall()
        self.check_interactable_collision()
        self.move()