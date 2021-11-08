import random
import json
import os

from pico2d import *
from mario_ob import *
from crash_check import *

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
    # 맵 디자인 할 방법
    # 여러 스테이지를 효율적으로 로들 할 수 있어야 한다.
    # 효율적으로 관리 할 수 있어야 한다. 효율적인게 뭔데?
    # 후보 1 map.py에서 위치의 배열을 가져와 생성
    # x, y, type의 튜플 배열을 만든다.
    enemys.append(Enemy(x=50))
    enemys.append(Enemy(x=600, type=1))
    for i in range(4):
        items.append(Item(x=100 + 100*i, y=250, type=i))
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
                # for enemy in enemys:
                #     enemy.is_alive = False
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

    # 충돌체크
    player_x_size, player_y_size = player.return_size()
    x3 = player.x - player_x_size / 2
    x4 = player.x + player_x_size / 2
    y3 = player.y - player_y_size / 2
    y4 = player.y + player_y_size / 2

    for item in items:
        x1 = item.x - item.x_size/2
        x2 = item.x + item.x_size/2
        y1 = item.y - item.y_size / 2
        y2 = item.y + item.y_size / 2

        if collision_check_2(x1, y1, x2, y2, x3, y3, x4, y4):
            if player.collision_with_item(item):
                item.__del__()

    for enemy in enemys:
        x1 = enemy.x - enemy.x_size / 2
        x2 = enemy.x + enemy.x_size / 2
        y1 = enemy.y - enemy.y_size / 2
        y2 = enemy.y + enemy.y_size / 2

        if collision_check_2(x1, y1, x2, y2, x3, y3, x4, y4):
            if player.collision_with_enemy(enemy):
                enemy.__del__()

def draw():
    clear_canvas()
    grass.draw()
    for enemy in enemys:
        enemy.draw()
    for item in items:
        item.draw(player.current_status)
    player.draw()

    player_x_size, player_y_size = player.return_size()
    x3 = player.x - player_x_size / 2
    x4 = player.x + player_x_size / 2
    y3 = player.y - player_y_size / 2
    y4 = player.y + player_y_size / 2

    item = items[2]
    x1 = item.x - item.x_size / 2
    x2 = item.x + item.x_size / 2
    y1 = item.y - item.y_size / 2
    y2 = item.y + item.y_size / 2
    debug_print('Is collision :' + str(collision_check_2(x1, y1, x2, y2, x3, y3, x4, y4)) + ', Type :' + str(item.type))

    update_canvas()
    delay(0.03)