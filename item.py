import random
from pico2d import *

import game_framework
import game_world

PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 10.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_COIN_ACTION = 8
FRAMES_PER_ACTION = 6


class Item:
    image_coin = None
    image_power = None
    image_star = None

    def __init__(self, x=random.randint(50, 750), y=random.randint(140, 550), type=0):
        self.type = type
        if Item.image_coin == None:
            Item.image_coin = load_image('sheet/items_sheet_coin.png')
        if Item.image_power == None:
            Item.image_power = load_image('sheet/items_sheet_power.png')
        if Item.image_star == None:
            Item.image_star = load_image('sheet/items_sheet_star.png')

        # 이미지

        if type == 0:
            self.image = Item.image_coin
        if type == 1:
            self.image = Item.image_power
        if type == 2:
            self.image = Item.image_star

        self.x = x
        self.y = y
        self.frame_delay = 0
        self.frame = 0
        self.is_alive = True

    def get_bb(self):
        if self.type == 0:
            return self.x - 12, self.y - 24, self.x + 12, self.y + 24
        else:
            return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def update(self):
        if self.frame_delay % 2 == 0:
            if self.type == 0:
                self.frame = (self.frame + 1) % 8
            elif self.type == 1 or self.type == 2:
                self.frame = (self.frame + 1) % 6
        self.frame_delay += 1

    def draw(self, player_status=0):
        if self.is_alive:
            if self.type == 0:
                self.image.clip_draw(8 * self.frame, 0, 8, 16, self.x, self.y, 24, 48) # 3배수 출력
            elif self.type == 1:
                if player_status == 0:
                    y_frame = 1
                else:
                    y_frame = 0
                self.image.clip_draw(16 * self.frame, y_frame*16, 16, 16, self.x, self.y, 48, 48)
            else:
                self.image.clip_draw(self.frame*16, 0, 16, 16, self.x, self.y, 48, 48)
