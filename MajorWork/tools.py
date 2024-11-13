#------------imports------------#
import pygame as pg
from constants import consts
from img_loader import img_loader
from id_mapping import id_map, name_id_map
#-------------------------------#

def get_pointer_position():
    mousePOS_x, mousePOS_y = pg.mouse.get_pos()
    mousePOS_y -= consts.bold_font_size * 1.5
    mousePOS_row = int((mousePOS_y + consts.player_y) / consts.cell_size)
    mousePOS_col = int((mousePOS_x + consts.player_x) / consts.cell_size)
    return mousePOS_row, mousePOS_col, mousePOS_x, mousePOS_y

def draw_gridlines():
    for x in range(0, consts.cell_count * consts.cell_size, consts.cell_size):
        pg.draw.line(consts.screen, consts.grid_colour, (x - consts.player_x, 0), (x - consts.player_x, consts.sheight))
    for y in range(int(consts.bold_font_size * 1.5), consts.cell_count * consts.cell_size, consts.cell_size):
        pg.draw.line(consts.screen, consts.grid_colour, (0, y - consts.player_y), (consts.swidth, y - consts.player_y))

def move_player(keys_pressed):
    if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
        if consts.player_y <= 0:
            consts.player_y = 0
            return
        consts.player_y -= consts.player_speed

    if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
        consts.player_y += consts.player_speed
        if consts.player_y + consts.sheight - consts.bold_font_size * 1.5 > consts.cell_count * consts.cell_size:
            consts.player_y = consts.cell_count * consts.cell_size - consts.sheight + consts.bold_font_size * 1.5

    if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
        if consts.player_x <= 0:
            consts.player_x = 0
            return
        consts.player_x -= consts.player_speed

    if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
        consts.player_x += consts.player_speed
        if consts.player_x + consts.swidth > consts.cell_count * consts.cell_size:
            consts.player_x = consts.cell_count * consts.cell_size - consts.swidth

def zoom(magnitude):
    # zoom in
    if magnitude > 0 and consts.sheight > (consts.cell_size * 10) < consts.swidth:
        consts.cell_size += 3

    # zoom out
    elif magnitude < 0:
        consts.cell_size -= 3
        if consts.sheight + consts.player_y > (consts.cell_size * consts.cell_count) or consts.swidth + consts.player_x > (consts.cell_size * consts.cell_count):
            consts.cell_size += 3
        if consts.player_x < 0:
            consts.player_x = 0
        if consts.player_y < 0:
            consts.player_y = 0
    # resize the images to the tile size
    img_loader.resize()

def machine_selector():
    alpha_surface = pg.Surface((consts.mselector_width, consts.mselector_height)).convert()

    # draw the translucent box
    alpha_surface.blit(consts.screen, ((consts.swidth-consts.mselector_width) / 2, consts.sheight-consts.mselector_height))
    alpha_surface.set_alpha(128)
    consts.screen.blit(alpha_surface, ((consts.swidth-consts.mselector_width) / 2, consts.sheight-consts.mselector_height))

    # draw the block on the selected machine
    selected = consts.machine_selection - id_map["conveyor"]
    x = (consts.mselector_width * selected / consts.machine_count) + (consts.swidth - consts.mselector_width) / 2
    y = consts.sheight-consts.mselector_height

    pg.draw.rect(consts.screen, consts.grid_colour, pg.Rect(x, y, consts.mselector_width / consts.machine_count, consts.mselector_height))

    # draw the machines and numbers
    for i in range(consts.machine_count):
        x = (consts.mselector_width * (i * 2 + 1) / (consts.machine_count*2)) + (consts.swidth - consts.mselector_width) / 2
        y = consts.sheight
        number = consts.vadodara_regular.render(str(i+1), True, pg.Color("white"))
        image = pg.transform.scale(img_loader.bank[name_id_map[i + id_map["conveyor"]]], (30, 30))
        consts.screen.blit(image, (x - image.get_size()[0] / 2, y - 35))
        consts.screen.blit(number, (x - number.get_size()[0] / 2, y - 60))
