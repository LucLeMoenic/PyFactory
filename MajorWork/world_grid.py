#------------imports------------#
from constants import consts
from numpy import zeros
from id_mapping import id_map, name_id_map
from img_loader import img_loader
from perlin import generate_ore_map
#-------------------------------#

class world():
    def __init__(self) :
        self.grid = zeros((consts.cell_count, consts.cell_count), dtype=int)
        self.ore_locations = []

        self.generate_ores()
        self.grid[0:60, 0:1] = id_map["border"]
        self.grid[0:1, 0:60] = id_map["border"]
        self.grid[59:60, 0:60] = id_map["border"]
        self.grid[0:60, 59:60] = id_map["border"]
        self.populate_ore_locations()

    def generate_ores(self):
        noise = generate_ore_map(60, 60)
        for x in range(len(noise)):
            for y in range(len(noise)):
                if noise[x][y] == 1:
                    self.grid[x][y] = id_map["coal_block"]
                if noise[x][y] == 2:
                    self.grid[x][y] = id_map["diamond_block"]
                if noise[x][y] == 3:
                    self.grid[x][y] = id_map["iron_block"]
    

    def populate_ore_locations(self):
        for row in range(consts.cell_count):
            for col in range(consts.cell_count):
                if self.grid[row, col] > 0:
                    self.ore_locations.append((row, col))

    def render(self):
        for coordinate in self.ore_locations:
            row, col = coordinate
            x = col * consts.cell_size - consts.player_x
            y = row * consts.cell_size - consts.player_y + consts.bold_font_size * 1.5
            consts.screen.blit(img_loader.scaled_bank[name_id_map[self.grid[row, col]]], (x, y))


world_grid = world()