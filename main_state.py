import random
import json
import os

from pico2d import *
from mario_ob import *

import game_framework
import title_state


name = "MainState"

player = None
enemys = None
items = None
grass = None
font = None


def enter():
    global player, enemys, items, grass
    player = Mario()
    enemys = []
    items = []

    enemys.append(Enemy(x=50))
    enemys.append(Enemy(x=600, type=1))
    for i in range(4):
        items.append(Item(x=100 + 100*i, y=400, type=i))
    grass = Grass()


def exit():
    global player, enemys, items, grass
    del(player)
    for enemy in enemys:
        del(enemy)
    for item in items:
        del(item)
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
                for enemy in enemys:
                    enemy.is_alive = False
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
    for enemy in enemys:
        enemy.update()
    for item in items:
        item.update()
    if not player.is_alive:
        if player.y < 0:
            game_framework.change_state(title_state)


def draw():
    clear_canvas()
    grass.draw()
    player.draw()
    for enemy in enemys:
        enemy.draw()
    for item in items:
        item.draw(player.current_status)
    update_canvas()
    delay(0.03)