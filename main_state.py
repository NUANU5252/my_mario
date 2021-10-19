import random
import json
import os

from pico2d import *
from mario_ob import *

import game_framework
import title_state



name = "MainState"

player = None
grass = None
font = None

def enter():
    global player, grass
    player = Mario()
    grass = Grass()


def exit():
    global player, grass
    del(player)
    del(grass)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_1:
                player.change_status()
            elif event.key == SDLK_2:
                player.change_status(False)
            elif event.key == SDLK_z:
                if player.attack_cool_time == 0:
                    player.attack()
            elif event.key == SDLK_RIGHT:
                player.is_right_key_down = True
            elif event.key == SDLK_LEFT:
                player.is_left_key_down = True
            elif event.key == SDLK_UP:
                player.is_up_key_down = True
            elif event.key == SDLK_DOWN:
                if not player.current_status == 0:
                    player.is_sit_down = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.is_right_key_down = False
            elif event.key == SDLK_LEFT:
                player.is_left_key_down = False
            elif event.key == SDLK_UP:
                player.is_up_key_down = False
                if player.is_jumping:
                    player.jump_count = 5
            elif event.key == SDLK_DOWN:
                player.is_sit_down = False


def update():
    player.update()
    if not player.is_alive:
        if player.y < 0:
            game_framework.change_state(title_state)

def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    update_canvas()
    delay(0.03)




