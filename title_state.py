import game_framework
from pico2d import *

import main_state
import game_world

name = "TitleState"
image = None


def enter():
    global image
    # image = load_image('start_state_image.jpeg')
    image = load_image('Super_Mario_Bros._Logo.svg.png')
    # 임시조치
    game_world.start_x = 0
    game_world.world_num = 1
    game_world.stage_num = 0


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.clip_draw(0, 0,  1200, 477, 400, 441, 800, 318)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






