import random
from pico2d import *

import game_framework
import game_world

PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 10.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# type에 따라서 이미지, 프레임등이 다름
# 0 굼바
# 1 엉금엉금


class Enemy:
    image_1 = None
    image_2 = None

    def __init__(self, x=random.randint(50, 750), y=90, type=0):
        self.type = type
        if Enemy.image_1 == None:
            Enemy.image_1 = load_image('sheet/enemies_sheet_1.png')
        if Enemy.image_2 == None:
            Enemy.image_2 = load_image('sheet/enemies_sheet_2.png')

        if type == 0:
            self.image = Enemy.image_1
        elif type == 1:
            self.image = Enemy.image_2
        self.x = x
        self.y = y

        # 현재 속도
        self.x_speed = RUN_SPEED_PPS
        self.y_speed = 0

        self.dir = 0 # 우, 좌
        self.dir_count = 2

        self.is_alive = True

        self.dead_count = 0

        self.frame = 0

    def get_bb(self):
        if self.type == 0:
            return self.x - 24, self.y - 48, self.x + 24, self.y
        elif self.type == 1:
            if self.is_alive:
                return self.x - 24, self.y - 48, self.x + 24, self.y + 24
            else:
                return self.x - 24, self.y - 48, self.x + 24, self.y - 6

    def del_self(self):
        if self.type == 0:
            if self.dead_count > 1:
                game_world.remove_object(self)
        elif self.type == 1:
            if self.dead_count > 10:
                game_world.remove_object(self)

    def alive_update(self):
        self.dir_count -= game_framework.frame_time
        if self.dir_count < 0:
            self.dir = (self.dir + 1) % 2
            self.dir_count = 2

        if self.dir == 0:
            self.x += self.x_speed * game_framework.frame_time
        else:
            self.x -= self.x_speed * game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION



    def update(self):
        if self.is_alive:
            self.alive_update()
        else:
            self.dead_count += game_framework.frame_time
            self.del_self()

    def draw(self):
        if not self.is_alive: # 사망
            self.image.clip_draw(16 * 4, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
        else:
            self.image.clip_draw(int(self.frame) * 16, self.dir*32, 16, 32, self.x, self.y, 48, 96)
