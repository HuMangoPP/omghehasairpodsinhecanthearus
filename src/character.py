import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, character_type, groups, obstacle_sprites):
        super().__init__(groups)
        self.character_type = character_type
        self.velocity = [0, 0]
        self.speed = 5
        self.acc = 0.25
        self.jump_speed = 15
        self.jumps = 1
        self.gravity = 0.5
        self.falling = [True, True]

        self.obstacle_sprites = obstacle_sprites

    def import_img(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=(100,500))
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if self.velocity[0]<self.speed:
                self.velocity[0]+=self.acc
        elif keys[pygame.K_a]:
            if self.velocity[0]>-self.speed:
                self.velocity[0]-=self.acc
        else:
            if self.velocity[0]>self.acc:
                self.velocity[0]-=self.acc
            elif self.velocity[0]<-self.acc:
                self.velocity[0]+=self.acc
            else:
                self.velocity[0] = 0
    

    def check_vertical_collision(self):
        self.rect.y+=1
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        self.rect.y-=1
        if colliding_sprites:
            if self.velocity[1]>0:
                self.rect.bottom=colliding_sprites[0].rect.top
                self.falling = [self.falling[1], False]
            elif self.velocity[1]<0:
                self.rect.top=colliding_sprites[0].rect.bottom
            self.velocity[1] = 0
            self.jumps = 1
        else:
            self.falling = [self.falling[1], True]

    def check_horizontal_collision(self):
        self.rect.y-=1
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        self.rect.y+=1
        if colliding_sprites:
            if self.velocity[0]>0:
                self.rect.right=colliding_sprites[0].rect.left
            elif self.velocity[0]<0:
                self.rect.left=colliding_sprites[0].rect.right

    def fall(self):
        if self.falling[0] and self.falling[1]:
            self.velocity[1]+=self.gravity

    def move(self):
        self.rect.x+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.y+=self.velocity[1]
        self.check_vertical_collision()

    def update(self):
        self.input()
        self.fall()
        self.move()