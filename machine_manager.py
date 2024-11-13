#------------imports------------#
import pygame as pg
from constants import consts
from id_mapping import id_map, name_id_map
from numpy import zeros
from img_loader import img_loader
from tools import get_pointer_position
from machines import machine
#-------------------------------#

class machine_manager_():
    def __init__(self):
        self.grid = zeros((consts.cell_count, consts.cell_count), dtype=object)
        self.machines_list = []
        self.item_list = []
        self.timer = 0

    # render all machines along with the translucent machine over the mouse position
    def render(self, tutorial_exit):
        row, col, mousePOS_x, mousePOS_y = get_pointer_position()
        x = col * consts.cell_size - consts.player_x
        y = row * consts.cell_size - consts.player_y + consts.bold_font_size * 1.5

        border_x1 = ((consts.swidth - consts.mselector_width) / 2)
        border_x2 = ((consts.swidth - consts.mselector_width) / 2 + consts.mselector_width)
        border_y = (consts.sheight - consts.mselector_height - consts.bold_font_size * 1.5)

        # rendering the translucent machine at mouse position
        if self.grid[(row, col)] != 0:
            pass
        # doesnt run if the mouse is above the title line
        elif mousePOS_y < 0:
            pass
        # doesnt run if the mouse is within the machine selector area
        elif border_x1 < mousePOS_x < border_x2 and mousePOS_y > border_y:
            pass
        # doesnt run if the mouse is over the upgrade button
        elif mousePOS_x > consts.swidth-128 and mousePOS_y > consts.sheight - 64 - consts.bold_font_size * 1.5:
            pass
        elif tutorial_exit == False:
            alpha_surface = pg.Surface((consts.cell_size, consts.cell_size)).convert()
            alpha_surface.blit(consts.screen, (-x, -y))
            alpha_surface.blit(pg.transform.rotate(img_loader.scaled_bank[name_id_map[consts.machine_selection]], consts.rotation_state), (0, 0))
            alpha_surface.set_alpha(128)        
            consts.screen.blit(alpha_surface, (x, y))

        for object in self.machines_list:
            if object.machine_type == id_map["conveyor"]:
                self.conveyor_render(object)
            else:
                row, col = object.row, object.col
                x = col * consts.cell_size - consts.player_x
                y = row * consts.cell_size - consts.player_y + consts.bold_font_size * 1.5
                consts.screen.blit(pg.transform.rotate(img_loader.scaled_bank[name_id_map[self.grid[row, col].machine_type]], self.grid[row, col].rotation), (x, y))

    def conveyor_render(self, object):
        clock = (0, 90, 180, 270)
        row, col = object.row, object.col
        x = col * consts.cell_size - consts.player_x
        y = row * consts.cell_size - consts.player_y + consts.bold_font_size * 1.5

        connections = [(row-1, col), (row, col-1), (row+1, col), (row, col+1)] # north, west, south, east 
        direction = int((object.rotation / 90)) # 0-in front, 1-left etc...

        # if behind is a conveyor and the direction is the same them print a normal conveyor
        if self.grid[connections[direction - 2]] != 0 and self.grid[connections[direction - 2]].rotation == object.rotation:
                image = img_loader.scaled_bank[name_id_map[object.machine_type]]
            
        # if the conveyor to the right is facing the current conveyor then print a turning conveyor clockwise
        elif self.grid[connections[direction - 1]] != 0 and self.grid[connections[direction - 1]].rotation == clock[direction - 3]:
                image = img_loader.scaled_bank["conveyor_cw"]

        # if the conveyor to the left is facing the current conveyor then print a turning conveyor counter clockwise
        elif self.grid[connections[direction - 3]] != 0 and self.grid[connections[direction - 3]].rotation == clock[direction - 1]:
                image = img_loader.scaled_bank["conveyor_ccw"]
            
        else:
            image = img_loader.scaled_bank[name_id_map[object.machine_type]]
        consts.screen.blit(pg.transform.rotate(image, object.rotation), (x, y))
            
    def place_machine(self, row, col):
        row, col, mousePOS_x, mousePOS_y = get_pointer_position()

        x1 = ((consts.swidth - consts.mselector_width) / 2)
        x2 = ((consts.swidth - consts.mselector_width) / 2 + consts.mselector_width)
        y = (consts.sheight - consts.mselector_height - consts.bold_font_size * 1.5)

        # doesnt run if the mouse is above the title line
        if mousePOS_y < 0:
            pass
        # doesnt run if the mouse is within the machine selector area
        elif x1 < mousePOS_x < x2 and mousePOS_y > y:
            pass
        # doesnt run if the mouse is over the upgrade button
        elif mousePOS_x > consts.swidth-128 and mousePOS_y > consts.sheight - 64 - consts.bold_font_size * 1.5:
            pass
        elif self.grid[row, col] == 0:
            connections = [(row-1, col), (row, col-1), (row+1, col), (row, col+1)]
            new_machine = machine(row, col, consts.rotation_state, consts.machine_selection, connections[int(consts.rotation_state/90)])
            self.grid[row, col] = new_machine
            self.machines_list.append(new_machine)
    
    def remove_machine(self, row, col):
        if self.grid[row, col] != 0:
            self.machines_list.remove(self.grid[row, col])
            self.grid[row, col] = 0

    def update_machines(self):
        self.timer += 1 

        for machine in self.machines_list: # every 10ms
            if machine.machine_type == id_map["miner"]:
                    new_item = machine.miner_action()
                    if new_item != False:
                        self.item_list.append(new_item)
                        new_item.direction = machine.rotation
        
        if self.timer > (99-consts.item_speed*1000):
            self.timer -= 100-consts.item_speed*1000

            for machine in self.machines_list: # every 1000ms
                machine.next_machine = self.grid[machine.next_machine_POS]
                if machine.machine_type == id_map["split_conveyor_left"] or machine.machine_type == id_map["split_conveyor_right"]:
                    swap = {0:1, 1:0}
                    machine.split_state = swap[machine.split_state]
                if machine.machine_type == id_map["furnace"]:
                    machine.furnace_action()

    def update_items(self):
        # resets the machines inventories
        for machine in self.machines_list:
            machine.inventory = []

        for item in self.item_list:
            machine_parent = self.grid[item.row, item.col]
            # reset the items in_inventory status
            item.in_inventory = False

            # find the next machine
            row = item.row
            col = item.col
            connections = [(row-1, col), (row, col-1), (row+1, col), (row, col+1)] # north, west, south, east
            direction = int((item.direction / 90)) # 0-in front, 1-left etc...
            next_machine = self.grid[connections[direction]]

            if next_machine != 0:
                item.next_machine = next_machine

            # if the item is not on a machine remove it
            if machine_parent == 0:
                self.item_list.remove(item)
            else:
                machine_parent.inventory.append(item)

                if item.next_machine != 0: # updates every item every 10ms
                    
                    furnace_open = True
                
                    # different move patterns for different machines
                    id = item.next_machine.machine_type
                    if id == id_map['conveyor'] or id == id_map['miner']:
                        direction = item.next_machine.rotation

                        
                    elif id == id_map['split_conveyor_left']:
                        direction = item.next_machine.rotation + item.next_machine.split_state * 90
                        if direction == 360:
                            direction = 0
                    
                    elif id == id_map['split_conveyor_right']:
                        direction = item.next_machine.rotation - item.next_machine.split_state * 90
                        if direction == -90:
                            direction = 270
                    
                    elif id == id_map['furnace']:
                        if len(item.next_machine.inventory) > 2:
                            furnace_open = False
                        direction = item.next_machine.rotation
                    
                    if machine_parent.machine_type == id_map["furnace"]:
                        for item in machine_parent.inventory:
                            item.in_inventory = True
                        machine_parent.inventory[0].in_inventory = False

                        if item.id == id_map["raw_iron"] or item.id == id_map["raw_coal"] or item.id == id_map["raw_diamond"]:
                            item.in_inventory = True
                    
                    if machine_parent.machine_type == id_map["seller"]:
                        self.item_list.remove(item)
                        consts.bank += consts.item_costs[item.id]
                    if furnace_open == True:    
                        item.move(direction)

    def render_items(self):     
        for item in self.item_list:
            image = img_loader.scaled_bank[name_id_map[item.id]]
            x = (item.col + item.tile_x) * consts.cell_size - consts.player_x
            y = (item.row + item.tile_y) * consts.cell_size - consts.player_y + consts.bold_font_size * 1.5
            if item.in_inventory == False:
                consts.screen.blit(image, (x, y))



machine_manager = machine_manager_()
