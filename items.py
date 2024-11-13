#------------imports------------#
from constants import consts
#-------------------------------#

class item():
    def __init__(self, item, col, row):
        self.id = item
        self.col = col
        self.row = row
        self.tile_x = 0
        self.tile_y = 0
        self.direction = 0
        self.next_machine = 0
        self.in_inventory = False
    
    def move(self, direction):
        # (-,-)-----(+,-)
        #   |         |
        #   |         |
        #   |         |
        # (-,+)-----(+,+)
        if self.in_inventory == False:
            if self.direction == 0: # north
                self.tile_y -= consts.item_speed # moving the item through the tile
                if self.tile_y < -1: # if the item moves out of the current tile
                    self.tile_y += 1
                    self.row -= 1
                    self.direction = direction

            if self.direction == 90: # west
                self.tile_x -= consts.item_speed
                if self.tile_x < -1:
                    self.tile_x += 1
                    self.col -= 1
                    self.direction = direction              

            if self.direction == 180: # south
                self.tile_y += consts.item_speed
                if self.tile_y > 1: 
                    self.tile_y -= 1
                    self.row += 1
                    self.direction = direction

            if self.direction == 270: # east
                self.tile_x += consts.item_speed
                if self.tile_x > 1: 
                    self.tile_x -= 1
                    self.col += 1
                    self.direction = direction
