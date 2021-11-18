import random
from pico2d import *
from crash_check import *

import game_framework
import main_state
import game_world

PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_COIN_ACTION = 8
FRAMES_PER_ACTION = 6

TIME_TAKES_TO_ACCELARATE = 0.3 # 초
Gravitational_acceleration_MPS = 10 / TIME_TAKES_TO_ACCELARATE# m/s
Gravitational_acceleration_PPS = Gravitational_acceleration_MPS * PIXEL_PER_METER

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
        self.start_y = y

        self.x_speed = RUN_SPEED_PPS / 2
        self.y_speed = 0

        self.dir = 1

        self.frame = 0
        self.is_ready = False # 아이템 소환이 끝나면 그때부터 상호작용이 가능하다.
        self.ready_count = 0

        self.live_time = 10

        if main_state.player.current_status == 0:
            self.power_type = 1
        else:
            self.power_type = 0

    def del_self(self):
        game_world.remove_object(self)

    def get_bb(self):
        if self.type == 0:
            return self.x - 12, self.y - 24, self.x + 12, self.y + 24
        else:
            return self.x - 24, self.y - 24, self.x + 24, self.y + 24

    def update_by_type(self):
        if self.type == 1:
            if self.power_type == 1:
                if self.x_speed > 0:
                    self.dir = 0
                else:
                    self.dir = 1
                self.x += self.x_speed * game_framework.frame_time

            # 중력가속도
            self.y_speed -= Gravitational_acceleration_PPS * game_framework.frame_time

            self.y += self.y_speed * game_framework.frame_time

        elif self.type == 2:
            if self.x_speed > 0:
                self.dir = 0
            else:
                self.dir = 1

            if self.live_time > 0:
                self.live_time -= game_framework.frame_time
            elif self.live_time <= 0:
                self.del_self()

            # 중력가속도
            self.y_speed -= Gravitational_acceleration_PPS * game_framework.frame_time
            # 위치 변경
            self.x += self.x_speed * game_framework.frame_time
            self.y += self.y_speed * game_framework.frame_time

    def collision_by_type(self, block):
        if self.type == 1:
            if abs(self.x - block.x) < abs(self.y - block.y):
                self.y_speed = 0
            else:
                self.x_speed *= -1
        elif self.type == 2:
            if abs(self.x - block.x) < abs(self.y - block.y):
                self.y_speed = RUN_SPEED_PPS * 1.5
            # 좌우 충돌 방향이 x 스피드 반사
            else:
                self.x_speed *= -1

    def collision_with_block(self, block):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = block.get_bb()

        col_dir = collide_direction(self, block)
        print(col_dir)
        if col_dir == 2:
           pass
        elif col_dir == 6:
            # self.x_speed = 0
            self.x += right_b - left_a
        elif col_dir == 4:
            # self.x_speed = 0
            self.x -= right_a - left_b
        elif col_dir == 8:
            self.y += top_b - bottom_a + 1
        elif col_dir == 5:
            pass
        self.collision_by_type(block)

    def crash_check(self):
        for block in game_world.objects[3]:
            if collide(self, block):
                self.collision_with_block(block)

    def update(self):
        if self.is_ready:
            if self.type == 0:
                self.frame = (self.frame + FRAMES_PER_COIN_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_COIN_ACTION
            else:
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.update_by_type()
            # 중력 영향과 충돌체크
            self.crash_check()
        elif not self.is_ready:
            self.y += game_framework.frame_time * 96
            self.ready_count += game_framework.frame_time
            if self.ready_count > 0.5:
                self.is_ready = True
                self.y = self.start_y + 48

    def draw(self):
        if self.type == 0:
            self.image.clip_draw(8 * int(self.frame), 0, 8, 16, self.x, self.y, 24, 48) # 3배수 출력
        elif self.type == 1:
            self.image.clip_draw(16 * int(self.frame), self.power_type*16, 16, 16, self.x, self.y, 48, 48)
        else:
            self.image.clip_draw(int(self.frame)*16, 0, 16, 16, self.x, self.y, 48, 48)
