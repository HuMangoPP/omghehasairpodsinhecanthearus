from tkinter import font
import pygame
from src.settings import *

def debug(display_surface, debug_msg, font):
    text = font.render(debug_msg, False, 'blue')
    text_box = text.get_rect(topleft = (TILESIZE, TILESIZE)).inflate(20, 20)
    display_surface.blit(text, text_box)