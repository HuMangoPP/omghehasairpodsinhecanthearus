import pygame, sys, os, json
from src.settings import *
from src.character import Character
from src.debug import debug
from src.tile import Tile
from src.player import Player
from src.interactable import Interactable

def create_sprite_dict(path, scale):
    # calls the import_spritesheets 
    sprite_dict = {}
    sprite_types = os.listdir(path)
    for sprite_type in sprite_types:
        sprites_list = os.listdir(path+'/'+sprite_type)
        sprite_dict[sprite_type] = []
        for sprite in sprites_list:
            if sprite.split('.')[1] == 'png':
                sprite = pygame.image.load(path+'/'+sprite_type+'/'+sprite).convert_alpha()
                sprite = pygame.transform.scale(sprite, (sprite.get_width()*scale, sprite.get_height()*scale))
                sprite_dict[sprite_type].append(sprite)
    return sprite_dict

def create_many_sprite_dicts(path, scale):
    sprite_dict = {}
    sprite_types = os.listdir(path)
    for sprite_type in sprite_types:
        sprites = create_sprite_dict(path+'/'+sprite_type, scale)
        sprite_dict[sprite_type] = sprites
    return sprite_dict

levels = []
current_level = 1

def load_levels(path):
    all_levels = os.listdir(path)
    print(os.getcwd())
    print(all_levels)
    for new_level in all_levels:
        with open(path+new_level) as level_file:
            level = json.load(level_file)
            levels.append(level)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("personal_gamejam_1")
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock();
    font = pygame.font.Font(FONT, 20)

    visible_sprites = pygame.sprite.Group()
    obstacle_sprites = pygame.sprite.Group()
    interactable_sprites = pygame.sprite.Group()

    player = Player('player', [visible_sprites], obstacle_sprites,interactable_sprites)
    player.import_img('./graphics/test/right_player.png')

    character = Character('character', [visible_sprites], obstacle_sprites,interactable_sprites)
    character.import_img('./graphics/test/koopa.png')

    interactable = Interactable([visible_sprites,interactable_sprites],'spring',obstacle_sprites,player)
    interactable.import_img('./graphics/test/spring.png')
    
    ground_img = pygame.image.load('./graphics/test/ground.png')
    ground_img = pygame.transform.scale(ground_img,(TILESIZE,TILESIZE))
    load_levels('./src/levels/')
    for row in levels[current_level]:
        for col in levels[current_level][row]:
            Tile([visible_sprites,obstacle_sprites],'ground',ground_img,int(col)*TILESIZE,int(row)*TILESIZE)

    player_pressed_jump = False
    jump_press_time = None
    jump_press_accepted_input = 200

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_pressed_jump = True
                    jump_press_time = pygame.time.get_ticks()
                elif event.key == pygame.K_j:
                    if player.holding_item!=None:
                        player.throw_interactable()
                    else:
                        player.pickup_interactable()
        if player_pressed_jump:
            if player.jumps>0:
                player.velocity[1] = -player.jump_speed
                player.jumps-=1
                player_pressed_jump = False
            elif pygame.time.get_ticks()-jump_press_time>jump_press_accepted_input:
                player_pressed_jump = False


        display_surface.fill('black')
        visible_sprites.draw(display_surface)
        interactable_sprites.draw(display_surface)
        visible_sprites.update()
        debug(display_surface, str(character.falling[0] and character.falling[1]),font)
        pygame.display.update()    
        clock.tick(FPS)
