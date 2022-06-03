import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, tile_type, image, x,y):
        super().__init__(groups)
        self.tile_type = tile_type
        self.image = pygame.Surface.copy(image)
        self.rect = self.image.get_rect(topleft=(x,y))
    
    