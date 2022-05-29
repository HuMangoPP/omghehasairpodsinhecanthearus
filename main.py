import pygame, sys
from src.settings import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("personal_gamejam_1")
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock();

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_surface.fill('black')
        pygame.display.update()    
        clock.tick(FPS)
        