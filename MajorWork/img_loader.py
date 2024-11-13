#------------imports------------#
import pygame as pg
from constants import consts
#-------------------------------#

class img_bank():
    def __init__(self):
        self.bank = {
            "coal_block":pg.image.load('images/coal_block.png'),
            "raw_coal":pg.image.load('images/raw_coal.png'),
            "refined_coal":pg.image.load('images/refined_coal.png'),
            "diamond_block":pg.image.load('images/diamond_block.png'),
            "raw_diamond":pg.image.load('images/raw_diamond.png'),
            "refined_diamond":pg.image.load('images/refined_diamond.png'),
            "iron_block":pg.image.load('images/iron_block.png'),
            "raw_iron":pg.image.load('images/raw_iron.png'),
            "refined_iron":pg.image.load('images/refined_iron.png'),

            "border":pg.image.load('images/border.png'),
            "furnace":pg.image.load('images/furnace.png'),
            "conveyor_ccw":pg.transform.rotate(pg.transform.flip(pg.image.load('images/conveyor_turn.png'), False, True), 180),
            "conveyor_cw":pg.image.load('images/conveyor_turn.png'),
            "split_conveyor_left":pg.image.load('images/split_conveyor_left.png'),
            "split_conveyor_right":pg.image.load('images/split_conveyor_right.png'),
            "conveyor":pg.image.load('images/conveyor.png'),
            "miner":pg.image.load('images/miner.png'),
            "seller":pg.image.load('images/seller.png'),

            "start_button":pg.image.load('images/start_button.png'),
            "menu_button":pg.image.load('images/menu_button.png'),
            "menu_button_hover":pg.image.load('images/menu_button_hover.png'),
            "tutorial_button":pg.image.load('images/tutorial_button.png'),
            "tutorial_button_hover":pg.image.load('images/tutorial_button_hover.png'),
            "tutorial_exit_button":pg.image.load('images/tutorial_exit_button.png'),
            "tutorial_previous_button":pg.image.load('images/arrow_button.png'),
            "tutorial_next_button":pg.transform.rotate(pg.transform.flip(pg.image.load('images/arrow_button.png'), False, True), 180),
            "speed_upgrade":pg.image.load('images/speed_upgrade.png'),
            "speed_upgrade_unavailable":pg.image.load('images/speed_upgrade_unavailable.png'),
        }
        self.resize()

    def resize(self):
        self.scaled_bank = dict()
        for name, image in self.bank.items():
            self.scaled_bank[name] = pg.transform.scale(image, (consts.cell_size, consts.cell_size))

img_loader = img_bank()