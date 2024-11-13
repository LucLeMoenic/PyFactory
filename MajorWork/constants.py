#------------imports------------#
import pygame as pg
from loader import get_resource_path
from id_mapping import id_map
#-------------------------------#

class constants():

    def __init__(self):
        self.fps = 60
        self.bank = 0

        self.player_x = 0
        self.player_y = 0
        self.swidth = 0
        self.sheight = 0

        self.player_speed = 20
        self.grid_lines_visible = True

        self.cell_size = 30
        self.cell_count = 60

        self.machine_selection = id_map["conveyor"]
        self.rotation_state = 0
        self.machine_count = 6
        self.item_speed = 0.004
        self.upgrade_cost = 1000

        self.mselector_width = 700
        self.mselector_height = 60

        self.load_fonts()
        self.load_colours()
        self.load_item_equivalences()
        self.load_item_costs()
    
    def load_fonts(self):
        pg.init()

        self.font_size = 18
        self.vadodara_regular = pg.font.Font(get_resource_path("fonts/HindVadodara-Medium.ttf"), self.font_size)

        self.bold_font_size = 32
        self.vadodara_medium = pg.font.Font(get_resource_path("fonts/HindVadodara-Regular.ttf"), self.bold_font_size)
    
    def load_colours(self):
        self.bg_colour = pg.Color("#143557") # dark blue
        self.grid_colour = pg.Color("#666666") # black

    def load_item_equivalences(self):
        self.item_equivalences = {
            id_map["coal_block"]:id_map["raw_coal"],
            id_map["iron_block"]:id_map["raw_iron"],
            id_map["diamond_block"]:id_map["raw_diamond"]
        }

    def load_item_costs(self):
        self.item_costs = {
            id_map["raw_coal"]:20,
            id_map["refined_coal"]:150,
            id_map["raw_iron"]:40,
            id_map["refined_iron"]:175,
            id_map["raw_diamond"]:100,
            id_map["refined_diamond"]:300,
        }

    def set_screen(self, screen):
        self.screen = screen
        self.swidth, self.sheight = self.screen.get_size()
    
    def set_clock(self, clock):
        self.clock = clock
    
    def cycle_rotation_state(self, magnitude):
        self.rotation_state += magnitude
        if self.rotation_state == 360:
            self.rotation_state = 0
        if self.rotation_state == -90:
            self.rotation_state = 270

consts = constants()