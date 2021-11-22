import random
from pico2d import *
from item import *

import game_framework
import game_world

PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
# 블럭에 속도는 없을지도?
# RUN_SPEED_KMPH = 10.0 # Km / Hour = 최대치
# RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
# RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
# RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Block:
    image_item_box = None
    image_block = None
    image_pipe = None
    image_flag_and_flagpole = None

    def __init__(self, x=random.randint(50, 750), y=random.randint(140, 550), type=0, item_queue = []):
        if Block.image_item_box == None:
            Block.image_item_box = load_image('sheet/block_sheet_item_box.png')
        if Block.image_block == None:
            Block.image_block = load_image('sheet/block_img.png')
        if Block.image_pipe == None:
            Block.image_pipe = load_image('sheet/pipe_img.png')
        if Block.image_flag_and_flagpole == None:
            Block.image_flag_and_flagpole = load_image('sheet/flag_and_flagpole.png')

        # 타입 0: 부셔지는 블럭, 1: 부셔지지 않는 블럭 = 아이템 박스, 2: 바닥 블럭, 3: 벽 블럭
        self.type = type
        self.x = x
        self.y = y
        self.frame = 0
        self. item_queue = [] + item_queue # 마리오가 박으면 배열 안의 아이템을 밷고 없으면 부셔지거나 이미지가 변한다.

    def collision_event(self, player):
        if len(self.item_queue) > 0:
            # 팝 해서 그 아이템 생성
            new_item_type = self.item_queue.pop(0)
            new_item = Item(self.x, self.y, new_item_type)
            game_world.add_object(new_item, 2)

            pass
        else:
            if self.type == 0 and player.current_status != 0:
                game_world.remove_object(self)

    def get_bb(self, start_x=0):
        return self.x - 24 - start_x, self.y - 24, self.x + 24 - start_x, self.y + 24

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self, start_x=0):
        # 타입과 큐의 상태에 따라서 달라진다.
        if self.type == 0:
            self.image_block.clip_draw(16 * 2, 0, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 1:
            if len(self.item_queue) > 0:
                self.image_item_box.clip_draw(16 * int(self.frame), 16, 16, 16, self.x - start_x, self.y, 48, 48)
            else:
                self.image_item_box.clip_draw(16 * int(self.frame), 0, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 2:
            self.image_block.clip_draw(16 * 0, 0, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 3:
            self.image_block.clip_draw(16 * 1, 0, 16, 16, self.x - start_x, self.y, 48, 48)



