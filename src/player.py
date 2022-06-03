import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, character_type, groups, obstacle_sprites,interactable_sprites):
        super().__init__(groups)
        self.character_type = character_type
        self.velocity = [0, 0]
        self.speed = 5
        self.acc = 0.4
        self.jump_speed = 15
        self.jumps = 1
        self.gravity = 0.5
        self.falling = [True, True]
        self.holding_item = None
        self.facing = 'right'
        self.throw_speed = 10

        self.obstacle_sprites = obstacle_sprites
        self.interactable_sprites=interactable_sprites

    def import_img(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=(100,500))
    
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
        self.rect.y+=1
        colliding_sprites = pygame.sprite.spritecollide(self,self.obstacle_sprites,False)
        if self.holding_item!=None:
            colliding_sprites.extend(pygame.sprite.spritecollide(self.holding_item,self.obstacle_sprites,False))
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
        if self.holding_item!=None:
            colliding_sprites.extend(pygame.sprite.spritecollide(self.holding_item,self.obstacle_sprites,False))
        self.rect.y+=1
        if colliding_sprites:
            if self.velocity[0]>0:
                self.rect.right=colliding_sprites[0].rect.left
            elif self.velocity[0]<0:
                self.rect.left=colliding_sprites[0].rect.right
            self.velocity[0]=0

    def fall(self):
        if self.falling[0] and self.falling[1]:
            self.velocity[1]+=self.gravity

    def pickup_interactable(self):
        interactables =  pygame.sprite.spritecollide(self,self.interactable_sprites,False)
        if interactables:
            interactables[0].picked_up=True
            self.holding_item = interactables[0]

    def throw_interactable(self):
        if self.facing=='right':
            self.holding_item.velocity[0]=self.throw_speed
        else:
            self.holding_item.velocity[0]=-self.throw_speed
        self.holding_item.picked_up=False
        self.holding_item = None

    def move(self):
        self.rect.x+=self.velocity[0]
        self.check_horizontal_collision()
        self.rect.y+=self.velocity[1]
        self.check_vertical_collision()

    def update(self):
        self.input()
        self.fall()
        self.move()