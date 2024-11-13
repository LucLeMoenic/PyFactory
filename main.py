#------------imports------------#
import pygame as pg
from constants import consts
from game_loop import game_loop
#-----------constrols-----------#
# e = rotate clockwise
# q = rotate anti-clockwise
# 1-9 = change selected machine
# g = turn grid lines on/off
# wasd/arrow keys = move screen
#-------------------------------#

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((960, 540))
    
    Icon = pg.image.load('images/menu_button.png')
    pg.display.set_icon(Icon)
    pg.display.set_caption('PyFactory')

    clock = pg.time.Clock()
    consts.set_clock(clock)
    consts.set_screen(screen)
    game_loop()