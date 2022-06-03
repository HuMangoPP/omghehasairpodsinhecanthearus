import pygame,sys,os
from settings import *
import json

level = {}

pygame.init()
pygame.display.set_caption("level editor")
display_surface = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

tiles = {
    './graphics/test/ground.png': pygame.image.load('./graphics/test/ground.png')
}
tile_name = './graphics/test/ground.png'

with open('./src/test.json') as json_file:
    level = json.load(json_file)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('./src/test.json','w') as outfile:
                json.dump(level,outfile)
            pygame.quit()
            sys.exit()
    
    if pygame.mouse.get_pressed(3)[0] or pygame.mouse.get_pressed(3)[1]:
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1] 
        for row in range(int(HEIGHT/TILESIZE+1)):
            if row in level:
                col_tiles = level[str(row)]
            else:
                col_tiles = {}
            for col in range(int(WIDTH/TILESIZE+1)):
                if mx>=col*TILESIZE and mx<(col+1)*TILESIZE and my>=row*TILESIZE and my<(row+1)*TILESIZE:
                    if pygame.mouse.get_pressed(3)[0]:
                        col_tiles[str(col)] = tile_name
                    elif pygame.mouse.get_pressed(3)[1] and str(col) in col_tiles:
                        del col_tiles[str(col)]
            level[row] = col_tiles

    display_surface.fill('black')
    for row in level:
        for col in level[str(row)]:
            img = tiles[level[str(row)][str(col)]]
            x = int(col)*TILESIZE
            y = int(row)*TILESIZE
            display_surface.blit(img,(x,y))
    pygame.display.update()
    clock.tick(FPS)
    

