import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, character_type, groups):
        super().__init__(groups)
        self.character_type = character_type
        self.velocity = [0, 0]
        self.speed = 5
        self.acc = 0.25
        self.jump_speed = 10

    def import_img(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=(100,100))
    
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
    
    def move(self):
        self.rect.x+=self.velocity[0]
        self.rect.y==self.velocity[1]

    def update(self):
        self.input()
        self.move()