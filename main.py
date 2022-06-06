import pygame, sys, os, json, math
from src.settings import *
from src.character import Character
from src.debug import debug
from src.tile import Tile
from src.player import Player
from src.interactable import Interactable

# creates a dictionary of list of sprites
def create_sprite_dict(path, scale):
    sprite_dict = {}
    sprite_types = os.listdir(path)
    for sprite_type in sprite_types:
        sprites_list = os.listdir(path+'/'+sprite_type)
        sprite_dict[sprite_type] = []
        for sprite in sprites_list:
            if sprite.split('.')[1] == 'png':
                sprite = pygame.image.load(path+'/'+sprite_type+'/'+sprite).convert_alpha()
                sprite = pygame.transform.scale(sprite, (scale, scale))
                sprite_dict[sprite_type].append(sprite)
    return sprite_dict

# load all .json file levels
def load_levels(path):
    levels = []
    all_levels = os.listdir(path)
    for new_level in all_levels:
        with open(path+new_level) as level_file:
            level = json.load(level_file)
            levels.append(level)
    return levels

# load the current level into sprite groups
def load_current_level(current_level):
    if current_level>0:
        visible_sprites.empty()
        visible_sprites.add(player)
        visible_sprites.add(character)
        visible_sprites.add(interactable)
        obstacle_sprites.empty()
    for i in range(len(levels)):
        for row in levels[current_level]:
            for col in levels[current_level][row]:
                Tile([visible_sprites,obstacle_sprites],'ground',tile_sprites,int(col)*TILESIZE,int(row)*TILESIZE)

# oscillation for tutorial buttons
def oscillation():
    time = pygame.time.get_ticks()
    value = math.sin(math.pi*time/1000)
    if value>=0:
        return 5
    else: 
        return 0

# transition from level to level
def transition(current_level):
    transition_surface = pygame.display.get_surface()
    radius = 0
    while radius<1500:
        pygame.draw.circle(transition_surface,'black',(WIDTH,HEIGHT-3*TILESIZE),radius)
        radius+=10
        pygame.display.update()
    current_level+=1
    current_level%=len(levels)
    player.reset()
    character.reset()
    interactable.reset()
    load_current_level(current_level)
    while radius>10:
        visible_sprites.draw(transition_surface)
        pygame.draw.circle(transition_surface,'black',(0,HEIGHT-3*TILESIZE),radius)
        radius-=10
        pygame.display.update()
    
    return current_level

if __name__ == '__main__':
    # initializing pygame
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("personal_gamejam_1")
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock();
    font = pygame.font.Font(FONT, FONT_SIZE)

    # importing assets
    mario_sprites = create_sprite_dict('./graphics/mario',TILESIZE)
    luigi_sprites = create_sprite_dict('./graphics/luigi',TILESIZE)
    spring_sprites = create_sprite_dict('./graphics/spring',TILESIZE)
    tile_sprites = create_sprite_dict('./graphics/tiles',TILESIZE)

    # loaded levels
    levels = load_levels('./src/levels/')
    current_level = 0

    # creating sprite groups
    visible_sprites = pygame.sprite.Group()
    obstacle_sprites = pygame.sprite.Group()
    interactable_sprites = pygame.sprite.Group()

    # loading the level
    load_current_level(current_level)

    # creating player, character, and item
    player = Player([visible_sprites], obstacle_sprites,interactable_sprites)
    character = Character([visible_sprites], obstacle_sprites,interactable_sprites)
    interactable = Interactable([visible_sprites,interactable_sprites],'spring',obstacle_sprites,player)
    player.import_img(luigi_sprites)
    character.import_img(mario_sprites)
    interactable.import_img(spring_sprites)

    # tutorial sprites
    arrow_keys = pygame.image.load('./graphics/tutorial/arrow_keys.png').convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys,(TILESIZE*3,TILESIZE*2))
    arrow_keys_rect = arrow_keys.get_rect()
    jump_key = pygame.image.load('./graphics/tutorial/jump_key.png').convert_alpha()
    jump_key = pygame.transform.scale(jump_key,(TILESIZE,TILESIZE))
    jump_key_rect = jump_key.get_rect()

    # player input 
    player_pressed_jump = False
    jump_press_time = None
    player_pressed_throw = False
    throw_press_time = None
    accepted_input_time = 200

    # defining values needed to start and end
    start_time = None
    highscores = {}
    with open('./src/highscores.json') as score_file:
        highscores = json.load(score_file)
    highscore_txt = []
    if 'best run' in highscores:
        highscore_txt.append('best run time: '+str(highscores['best run'][0]))
        highscore_txt.append('best run mario death: '+str(highscores['best run'][1]))
        highscore_txt.append('best run luigi death: '+str(highscores['best run'][2]))
        highscore_txt.append('best run spring use: '+str(highscores['best run'][3]))
    highscore_render = []
    highscore_box = []
    for i in range(len(highscore_txt)):
        msg = font.render(highscore_txt[i],False,'white')
        highscore_render.append(msg)
        highscore_box.append(msg.get_rect(topleft=(20,20+i*(FONT_SIZE+10))))

    title_screen_msgs = ["A regular day for Luigi-- but, what is that!?",
    "Mario is walking into that hole!",
    "ohmygodmariohasairpodsin!!",
    "He can't hear us! We have to go help him!",
    "Let's make sure he gets back home safety.",
    "With this trusty spring, I can make sure he can",
    "leap over any obstacle!",]
    title_screen_txt = []
    txt_boxes = []
    for i in range(len(title_screen_msgs)):
        render_msg = font.render(title_screen_msgs[i],False,'white')
        title_screen_txt.append(render_msg)
        txt_boxes.append(render_msg.get_rect(center=(WIDTH//2,200+i*(FONT_SIZE+10))))

    end_screen_msg = "Thank you for bringing Mario to home safetly!"
    end_screen_txt = font.render(end_screen_msg,False,'white')
    end_screen_box = end_screen_txt.get_rect(center=(WIDTH//2,300))
    end_stats = None
    end_stats_msgs = []
    end_stats_boxes = []    

    # game logic
    paused = False
    can_restart = False

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exit pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not paused:
                # player input
                if event.key == pygame.K_w:
                    player_pressed_jump = True
                    jump_press_time = pygame.time.get_ticks()
                if event.key == pygame.K_j:
                    player_pressed_throw = True
                    throw_press_time = pygame.time.get_ticks()
                if event.key == pygame.K_r and can_restart:
                    paused = True
                    current_level = transition(current_level)
                    paused = False
        
        # jump input leniency
        if player_pressed_jump and not paused:
            if player.jumps>0:
                player.velocity[1] = -player.jump_speed
                player.jumps-=1
                player_pressed_jump = False
            if pygame.time.get_ticks()-jump_press_time>accepted_input_time:
                player_pressed_jump = False

        # throw/pickup input leniency
        if player_pressed_throw:
            if player.holding_item==None:
                player.pickup_interactable()
                player_pressed_throw = False
            else:
                player.throw_interactable()
                player_pressed_throw = False
            if pygame.time.get_ticks()-throw_press_time>accepted_input_time:
                player_pressed_jump = False

        # makes sure game is running
        if not paused:
            # checks if mario has reached the goal for each level
            if character.check_goal():
                paused = True
                current_level = transition(current_level)
                paused = False
            
            # draw and update sprites
            display_surface.fill('black')
            visible_sprites.update(current_level)
            visible_sprites.draw(display_surface)

            # if game has just started, first level, show text and tutorial
            if current_level==0:
                for i in range(len(title_screen_txt)):
                    display_surface.blit(title_screen_txt[i],txt_boxes[i])
                arrow_keys_rect.bottomright = player.rect.topleft
                jump_key_rect.bottomleft = player.rect.topright
                arrow_keys_rect.bottom += oscillation()
                jump_key_rect.bottom += oscillation()
                display_surface.blit(arrow_keys,arrow_keys_rect)
                display_surface.blit(jump_key,jump_key_rect)
                start_time = pygame.time.get_ticks()

            # if game has ended, last level, show scores
            if current_level==len(levels)-1:
                if end_stats==None:
                    end_time = pygame.time.get_ticks()
                    end_stats = ["This run took " + str(end_time-start_time) + " ms",
                    "Mario died "+str(character.deaths)+ " times",
                    "Luigi died "+str(player.deaths)+" times",
                    "Spring thrown away "+str(interactable.deaths)+" times"
                    ]
                    for i in range(len(end_stats)):
                        end_msg = font.render(end_stats[i],False,'white')
                        end_stats_msgs.append(end_msg)
                        end_stats_boxes.append(end_msg.get_rect(center=(WIDTH/2,300+(i+1)*(FONT_SIZE+10))))
                    scores = {}
                    with open('./src/highscores.json') as scores_file:
                        scores = json.load(scores_file)
                    if 'best run' in scores:
                        best_run = scores['best run']
                        if end_time-start_time<best_run[0] and character.deaths<best_run[1] and player.deaths<best_run[2] and interactable.deaths<best_run[3]:
                            scores['best run'] = [end_time-start_time, character.deaths, player.deaths, interactable.deaths]
                    else: 
                        scores['best run'] = [end_time-start_time, character.deaths, player.deaths, interactable.deaths]
                    
                    if 'best parts' in scores:
                        best_parts = scores['best_parts']
                        if end_time-start_time<best_run[0]:
                            scores['best parts'][0] = end_time-start_time
                        if character.deaths<best_run[1]:
                            scores['best parts'][1] = character.deaths
                        if player.deaths<best_run[2]:
                            scores['best parts'][2] = player.deaths
                        if interactable.deaths<best_run[3]:
                            scores['best parts'][3] = player.deaths
                    else:
                        scores['best run'] = [end_time-start_time, character.deaths, player.deaths, interactable.deaths]
                    
                    with open('./src/highscores.json', 'w') as out:
                        json.dump(scores,out)
                can_restart = True
                display_surface.blit(end_screen_txt,end_screen_box)
                for i in range(len(end_stats_msgs)):
                    display_surface.blit(end_stats_msgs[i],end_stats_boxes[i])
        
        # display high scores
        for i in range(len(highscore_render)):
            display_surface.blit(highscore_render[i],highscore_box[i])

        # update
        pygame.display.update()    
        clock.tick(FPS)
