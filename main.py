import pygame, sys
from src.settings import *
from src.character import Character
from src.debug import debug

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("personal_gamejam_1")
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock();
    font = pygame.font.Font(FONT, 20)

    visible_sprites = pygame.sprite.Group()

    player = Character('player', [visible_sprites])
    player.import_img('./graphics/test/right_player.png')


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_surface.fill('black')
        visible_sprites.draw(display_surface)
        visible_sprites.update()
        debug(display_surface, str(player.velocity[0]),font)
        pygame.display.update()    
        clock.tick(FPS)
