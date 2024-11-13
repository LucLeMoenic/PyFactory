#------------imports------------#
import pygame as pg
from img_loader import img_loader
from id_mapping import id_map, name_id_map
from constants import consts
#-------------------------------#

class button():
    def __init__(self, x, y, id, scale):
        self.id = id
        image = img_loader.bank[id]
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        consts.screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def check_collision(self):
        POS = pg.mouse.get_pos()
        if self.rect.collidepoint(POS):
            return True
        return False


class button_manager_():

    def create_buttons(self):
        self.start_button = button(consts.swidth*2/5, 250, "start_button", 7)
        self.exit_button = button(consts.swidth*2/5, 360, "start_button", 7)
        self.main_menu_buttons = [self.start_button, self.exit_button]

        self.settings = button(consts.swidth - 60, (consts.bold_font_size*1.5-32*1.2)/2, "menu_button", 1.2)
        self.tutorial = button(consts.swidth - 120, (consts.bold_font_size*1.5-32*1.2)/2, "tutorial_button", 1.2)

        self.settings_hover = button(consts.swidth - 60, (consts.bold_font_size*1.5-32*1.2)/2, "menu_button_hover", 1.2)
        self.tutorial_hover = button(consts.swidth - 120, (consts.bold_font_size*1.5-32*1.2)/2, "tutorial_button_hover", 1.2)

        self.tutorial_exit = button(consts.swidth - 220, 70, "tutorial_exit_button", 2)
        self.tutorial_next = button(consts.swidth/2 + 100, 380, "tutorial_next_button", 2)
        self.tutorial_previous = button(consts.swidth/2 - 164, 380, "tutorial_previous_button", 2)

        self.item_speed_upgrade = button(consts.swidth-128, consts.sheight-64, "speed_upgrade", 1)
        self.item_speed_upgrade_unavailable = button(consts.swidth-128, consts.sheight-64, "speed_upgrade_unavailable", 1)

        self.game_buttons = []
        for i in range(0, consts.machine_count):
            x = (consts.mselector_width * i / consts.machine_count) + (consts.swidth - consts.mselector_width) / 2
            y = consts.sheight-consts.mselector_height
            new_button = button(x, y, (name_id_map[i + id_map["conveyor"]]), 3.5)
            self.game_buttons.append(new_button)

    def draw_game_buttons(self):
        self.settings.draw()
        self.tutorial.draw()


    def machine_selector_collision(self):
        for button in self.game_buttons:
            if button.check_collision():
                return button.id
        return False

button_manager = button_manager_()