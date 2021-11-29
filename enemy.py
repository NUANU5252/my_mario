import random
from pico2d import *
from crash_check import *
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

import game_framework
import game_world

PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

TIME_TAKES_TO_ACCELARATE = 0.3 # 초
Gravitational_acceleration_MPS = 10 / TIME_TAKES_TO_ACCELARATE# m/s
Gravitational_acceleration_PPS = Gravitational_acceleration_MPS * PIXEL_PER_METER

# type에 따라서 이미지, 프레임등이 다름
# 0 굼바
# 1 엉금엉금


class Enemy:
    image_1 = None
    image_2 = None

    def __init__(self, x=random.randint(50, 750), y=90, type_=0):
        self.patrol_order = 1
        self.patrol_positions = []
        self.patrol_positions.append((x, y))
        self.patrol_positions.append((x + RUN_SPEED_PPS, y) )
        self.x, self.y = self.patrol_positions[0]  # 시작 위치는 0, 다음 위치는 1
        self.type = type_
        if Enemy.image_1 == None:
            Enemy.image_1 = load_image('sheet/enemies_sheet_1.png')
        if Enemy.image_2 == None:
            Enemy.image_2 = load_image('sheet/enemies_sheet_2.png')
        if self.type == 0:
            self.image = Enemy.image_1
        elif self.type == 1:
            self.image = Enemy.image_2
        # 현재 속도
        self.x_speed = RUN_SPEED_PPS / 2
        self.y_speed = 0
        self.dir = 0 # 우, 좌
        self.dir_count = 2
        self.is_alive = True
        self.dead_count = 0
        self.frame = 0
        self.build_behavior_tree()

    def build_behavior_tree(self):
        pass

    def get_bb(self, start_x=0):
        if self.type == 0:
            return self.x - 24 - start_x, self.y - 48, self.x + 24 - start_x, self.y
        elif self.type == 1:
            if self.is_alive:
                return self.x - 24 - start_x, self.y - 48, self.x + 24 - start_x, self.y + 24
            else:
                return self.x - 24 - start_x, self.y - 48, self.x + 24 - start_x, self.y - 6

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

        self.y_speed -= Gravitational_acceleration_PPS * game_framework.frame_time

        if self.dir == 0:
            self.x += self.x_speed * game_framework.frame_time
        else:
            self.x -= self.x_speed * game_framework.frame_time
        self.y += self.y_speed * game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.crash_check()

    def crash_check(self):
        for block in game_world.objects[3]:
            if collide(self, block):
                self.collision_with_block(block)

    def collision_with_block(self, block):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = block.get_bb()

        col_dir = collide_direction(self, block)
        # print(col_dir)
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
        if abs(self.x - block.x) < abs(self.y - block.y):
            self.y_speed = 0
        else:
            self.dir = (self.dir + 1) % 2

    def update(self):
        if self.is_alive:
            self.alive_update()
        else:
            self.dead_count += game_framework.frame_time
            self.del_self()

    def draw(self, start_x=0):
        if not self.is_alive: # 사망
            self.image.clip_draw(16 * 4, self.dir * 32, 16, 32, self.x - start_x, self.y, 48, 96)
        else:
            self.image.clip_draw(int(self.frame) * 16, self.dir*32, 16, 32, self.x - start_x, self.y, 48, 96)
