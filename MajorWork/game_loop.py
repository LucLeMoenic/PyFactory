#------------imports------------#
import pygame as pg
from constants import consts
from tools import *
from world_grid import world_grid
from id_mapping import id_map
from machine_manager import machine_manager
from buttons import button_manager
#-------------------------------#


def game_loop():
    # used in the start menu
    title = consts.vadodara_regular.render("PyFactory", True, pg.Color("white"))

    # creates an event in pygame
    # timer for machine and item updates
    machine_update = pg.USEREVENT + 1
    # event called machine_updates sent every 10ms
    pg.time.set_timer(machine_update, 10)

    # creates the buttons
    button_manager.create_buttons() 

    # loading the images that arent in the image loader as all those are scaled to tile size
    background = pg.image.load('images/start_background.png')
    tutorial_page_1 = pg.transform.scale(pg.image.load('images/tutorial_page_1.png'), (640, 360))
    tutorial_page_2 = pg.transform.scale(pg.image.load('images/tutorial_page_2.png'), (640, 360))
    bank_balance = pg.image.load('images/bank_balance.png')
    speed_balance = pg.image.load('images/speed_balance.png')
    
    game_state = "start_menu"
    tutorial_open = True
    current_tutorial_page = tutorial_page_1

    while True:
        
        if game_state == "start_menu":
            consts.screen.blit(pg.transform.scale(background, (consts.swidth, consts.sheight)), (0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                    if event.key == pg.K_SPACE:
                        game_state = "game"
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0]:
                        if button_manager.start_button.check_collision():
                            game_state = "game"
                        if button_manager.exit_button.check_collision():
                            return


        if game_state == "game":
            consts.clock.tick(consts.fps)
            mousePOS_row, mousePOS_col, mousePOS_x, mousePOS_y = get_pointer_position()
            move_player(pg.key.get_pressed())
            
            consts.screen.fill(consts.bg_colour)
            if consts.grid_lines_visible:
                draw_gridlines()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                if event.type == pg.MOUSEBUTTONDOWN:
                    
                    if pg.mouse.get_pressed()[0]: # right click
                        if tutorial_open == False:
                            machine_manager.place_machine(mousePOS_row, mousePOS_col)

                        collision = button_manager.machine_selector_collision()
                        if collision != False:
                            consts.machine_selection = id_map[collision]
                        
                        collision = button_manager.settings.check_collision()
                        if collision != False:
                            game_state = "start_menu"

                        collision = button_manager.tutorial.check_collision()
                        if collision != False:
                            tutorial_open = True
                        
                        collision = button_manager.tutorial_exit.check_collision()
                        if collision != False:
                            tutorial_open = False
                        
                        collision = button_manager.item_speed_upgrade.check_collision()
                        if collision != False and consts.bank > consts.upgrade_cost:
                            consts.item_speed *= 1.1
                            consts.bank -= consts.upgrade_cost
                            consts.upgrade_cost *= 2
                        
                        if tutorial_open == True:
                            collision = button_manager.tutorial_next.check_collision()
                            if current_tutorial_page == tutorial_page_1:
                                if collision!= False:
                                    current_tutorial_page = tutorial_page_2
                            collision = button_manager.tutorial_previous.check_collision()
                            if current_tutorial_page == tutorial_page_2:
                                if collision!= False:
                                    current_tutorial_page = tutorial_page_1

                    
                    if pg.mouse.get_pressed()[2]: # left click
                        machine_manager.remove_machine(mousePOS_row, mousePOS_col)

                if event.type == machine_update:
                    if tutorial_open == False:
                        machine_manager.update_machines()
                        machine_manager.update_items()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_state = "start_menu"

                    # remove gridlines
                    if event.key == pg.K_g:
                        if consts.grid_lines_visible == False:
                            consts.grid_lines_visible = True
                        else:
                            consts.grid_lines_visible = False
                    
                    # changing the selected machine 
                    if pg.K_0 < event.key < pg.K_7:
                        consts.machine_variation_state = 0
                        consts.machine_selection = event.key - pg.K_0 + id_map["conveyor"] - 1

                    # cycling the rotation state
                    if event.key == pg.K_e or event.key == pg.K_q:
                        rotation = 90 if event.key == pg.K_q else -90
                        consts.cycle_rotation_state(rotation)

                # zoom in/out screen
                if event.type == pg.MOUSEWHEEL:
                    zoom(event.y)

            world_grid.render()
            machine_manager.render(tutorial_open)

            machine_manager.render_items()

            machine_selector()

            # title bar
            pg.draw.rect(consts.screen, pg.Color("black"), (0, 0, consts.swidth, consts.bold_font_size * 1.5))
            consts.screen.blit(title, ((consts.swidth - title.get_width()) / 2, consts.bold_font_size / 3))
            button_manager.draw_game_buttons()
            button_manager.item_speed_upgrade.draw()
            if consts.bank < consts.upgrade_cost:
                button_manager.item_speed_upgrade_unavailable.draw()

            # money bar
            balance = consts.vadodara_regular.render(str(int(consts.bank)), True, pg.Color("black"))
            consts.screen.blit(bank_balance, (20, consts.bold_font_size / 4))
            consts.screen.blit(balance, (70, consts.bold_font_size / 2.4))

            # speed bar
            speed = consts.vadodara_regular.render(str(round(consts.item_speed*1000, 2)), True, pg.Color("black"))
            consts.screen.blit(speed_balance, (160, consts.bold_font_size / 4))
            consts.screen.blit(speed, (210, consts.bold_font_size / 2.4))

            # speed upgrade button
            upgrade = consts.vadodara_regular.render(str(int(consts.upgrade_cost)), True, pg.Color("black"))
            consts.screen.blit(upgrade, (consts.swidth - 90, consts.sheight-38))

            collision = button_manager.settings.check_collision()
            if collision != False:
                button_manager.settings_hover.draw()

            collision = button_manager.tutorial.check_collision()
            if collision != False:
                button_manager.tutorial_hover.draw()
            
            if tutorial_open == True:
                consts.screen.blit(current_tutorial_page, (160,80))

        pg.display.flip()