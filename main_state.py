import random
import json
import os

from pico2d import *
from mario_ob import *
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
start_x = 0


def enter():
    global player, start_x

    player = mario.Mario()
    map.world_1_1()
#     플레이어 포함 보류
    start_x = 0


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
        #     elif event.key == SDLK_1:
        #         player.change_status()
        #     elif event.key == SDLK_2:
        #         player.change_status(False)
        #         # for enemy in enemys:
        #         #     enemy.is_alive = False
        #     elif event.key == SDLK_z:
        #         if player.attack_cool_time == 0:
        #             player.attack()
        #     elif event.key == SDLK_RIGHT:
        #         player.is_right_key_down = True
        #     elif event.key == SDLK_LEFT:
        #         player.is_left_key_down = True
        #     elif event.key == SDLK_UP:
        #         player.is_up_key_down = True
        #     elif event.key == SDLK_DOWN:
        #         if not player.current_status == 0:
        #             player.is_sit_down = True
        # elif event.type == SDL_KEYUP:
        #     if event.key == SDLK_RIGHT:
        #         player.is_right_key_down = False
        #     elif event.key == SDLK_LEFT:
        #         player.is_left_key_down = False
        #     elif event.key == SDLK_UP:
        #         player.is_up_key_down = False
        #         if player.is_jumping:
        #             player.jump_count = 5
        #     elif event.key == SDLK_DOWN:
        #         player.is_sit_down = False


def update():
    global start_x

    player.update()
    for game_object in game_world.all_objects():
        game_object.update()
        # try:
        #     game_object.update()
        # except:
        #     print('game_object: ', game_object.__name__)

    if not player.is_alive:
        if player.y < 0:
            game_framework.change_state(title_state)

    if player.x - start_x > 400:
        start_x += player.x - start_x - 400

    if player.x - start_x < 48:
        player.x = start_x + 48


def draw():
    clear_canvas()
    # grass.draw()
    # for enemy in enemys:
    #     enemy.draw()
    # for item in items:
    #     item.draw(player.current_status) # 개선 필요
    for game_object in game_world.all_objects():
        try:
            game_object.draw(start_x)
            if draw_bb:
                draw_rectangle(*game_object.get_bb(start_x))
        except:
            # pass
            print('game_object: ', game_object.__name__)
    player.draw(start_x)
    if draw_bb:
        draw_rectangle(*(player.get_bb(start_x)))

    debug_print('cur_state:' + str(player.cur_state) + 'x_speed:' + str(player.x_speed)
                + 'x_acceleration:' + str(player.x_acceleration))

    update_canvas()
