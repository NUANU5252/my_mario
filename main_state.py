import random
import json
import os

from pico2d import *
# from mario_ob import *
from crash_check import *

import mario
import game_framework
import title_state
import map
import game_world

name = "MainState"

player = None
font = None

draw_bb = False

# 그림이 그려지기 시작하는 x
# start_x = 0


def enter():
    global player

    player = mario.Mario()
    map.load_world()


def exit():
    global player
    del(player)
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global draw_bb
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            if draw_bb:
                draw_bb = False
            else:
                draw_bb = True
        else:
            player.handle_event(event)


def update():
    # global start_x

    player.update()
    for game_object in game_world.all_objects():
        # game_object.update()
        try:
            if game_world.start_x - 48*game_world.Update_range < game_object.x < game_world.start_x + 48*game_world.Update_range + 800:
                game_object.update()
            elif game_world.start_x - 48*10 > game_object.x:
                game_world.remove_object(game_object)
        except:
            print('game_object: ', game_object.__name__)

    if not player.is_alive:
        if player.die_count < 0:
            map.load_world(1)
            pass

    if player.x - game_world.start_x > 400 and game_world.start_x < game_world.max_start_x:
        game_world.start_x += player.x - game_world.start_x - 400

    if player.x - game_world.start_x < 48:
        player.x = game_world.start_x + 48


def draw():
    clear_canvas()
    game_world.Basic_bgi.clip_draw(0, 0, 48, 48, 48*8, 48*6, 48*16, 48*12)

    for game_object in game_world.all_objects():
        try:
            if game_world.start_x - 48 < game_object.x < game_world.start_x + 48 + 800:
                game_object.draw(game_world.start_x)
                if draw_bb:
                    draw_rectangle(*game_object.get_bb(game_world.start_x))
        except:
            print('game_object: ', game_object.__name__)
        #     pass
    player.draw(game_world.start_x)
    if draw_bb:
        draw_rectangle(*(player.get_bb(game_world.start_x)))

    debug_print('cur_state:' + str(player.cur_state) + 'x_speed:' + str(player.x_speed)
                + 'x_acceleration:' + str(player.x_acceleration))

    update_canvas()
