#------------imports------------#
from id_mapping import id_map
from world_grid import world_grid
from items import item
from constants import consts
#-------------------------------#

class machine():
    def __init__(self, row, col, rotation, machine_type, next_machine):
        self.row = row
        self.col = col
        self.rotation = rotation
        self.machine_type = machine_type
        self.split_state = 0

        self.inventory = []
        self.old_inventory = []
        self.next_machine = 0
        self.next_machine_POS = next_machine

    def miner_action(self):
        if len(self.inventory) < 1:
            grid_value = world_grid.grid[self.row, self.col]
            if grid_value != 0:
                return item(consts.item_equivalences[grid_value], self.col, self.row)
        return False
    
    def furnace_action(self):
        if len(self.inventory) > 1:
            item = self.inventory[0]
            next_item = self.inventory[1]
            if item.id == id_map["refined_iron"]:
                if next_item.id == id_map["raw_iron"]:
                    next_item.id = id_map["refined_iron"]
            if item.id == id_map["refined_diamond"]:
                if next_item.id == id_map["raw_diamond"]:
                    next_item.id = id_map["refined_diamond"]
            if item.id == id_map["refined_coal"]:
                if next_item.id == id_map["raw_coal"]:
                    next_item.id = id_map["refined_coal"]

        if len(self.inventory) > 0:
            item = self.inventory[0]
            if item.id == id_map["raw_iron"]:
                item.id = id_map["refined_iron"]
            if item.id == id_map["raw_diamond"]:
                item.id = id_map["refined_diamond"]
            if item.id == id_map["raw_coal"]:
                item.id = id_map["refined_coal"] 