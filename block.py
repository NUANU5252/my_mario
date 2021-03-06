import random
from pico2d import *
from item import *

import game_framework
import game_world
import map

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
    image_horizontal_pipe_1 = None
    image_horizontal_pipe_2 = None

    Break_sound = None

    def __init__(self, x=random.randint(50, 750), y=random.randint(140, 550), type=0, item_queue = []):
        if Block.image_item_box == None:
            Block.image_item_box = load_image('sheet/block_sheet_item_box.png')
        if Block.image_block == None:
            Block.image_block = load_image('sheet/block_img.png')
        if Block.image_pipe == None:
            Block.image_pipe = load_image('sheet/pipe_img.png')
        if Block.image_flag_and_flagpole == None:
            Block.image_flag_and_flagpole = load_image('sheet/flag_and_flagpole.png')
        if Block.image_horizontal_pipe_1 == None:
            Block.image_horizontal_pipe_1 = load_image('sheet/horizontal_pipe_img_1.png')
        if Block.image_horizontal_pipe_1 == None:
            Block.image_horizontal_pipe_1 = load_image('sheet/horizontal_pipe_img_2.png')

        if Block.Break_sound == None:
            Block.Break_sound = load_wav('sound/Stomp 2.wav')
            Block.Break_sound.set_volume(game_world.Object_volume)

        # 타입 0: 부셔지는 블럭, 1: 부셔지지 않는 블럭 = 아이템 박스, 2: 바닥 블럭, 3: 벽 블럭, 4: 토관, 5: 깃발, 6,7:수평 토관
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
                Block.Break_sound.play()

    def pipe_event(self):
        # 플레이어가 자신의 위에서 sit_state라면
        print('pipe event---')
        if len(self.item_queue) == 0:
            pass
        else:
            map.load_world(2)
            pass

    def get_bb(self, start_x=0):
        if self.type == 5:
            return self.x - 1 - start_x, self.y - 24, self.x + 5 - start_x, self.y + 432 # 9.5 * 16 * 3 - 24
        elif self.type == 6:
            return self.x - 48 - start_x, self.y - 24, self.x + 48 - start_x, self.y + 72
        elif self.type == 7:
            return self.x - 1 - start_x, self.y - 24, self.x + 5 - start_x, self.y + 432
        elif self.type == 4:
            return self.x - 48 - start_x, self.y - 96, self.x + 48 - start_x, self.y + 96
        else:
            return self.x - 24 - start_x, self.y - 24, self.x + 23 - start_x, self.y + 23

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self, start_x=0):
        # 타입과 큐의 상태에 따라서 달라진다.
        if game_world.is_underground:
            draw_type = 1
        else:
            draw_type = 0

        if self.type == 0:
            self.image_block.clip_draw(16 * 2, draw_type * 16, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 1:
            if len(self.item_queue) > 0:
                self.image_item_box.clip_draw(16 * int(self.frame), 16, 16, 16, self.x - start_x, self.y, 48, 48)
            else:
                self.image_item_box.clip_draw(16 * int(self.frame), 0, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 2:
            self.image_block.clip_draw(16 * 0, draw_type * 16, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 3:
            self.image_block.clip_draw(16 * 1, draw_type * 16, 16, 16, self.x - start_x, self.y, 48, 48)
        elif self.type == 4:
            self.image_pipe.clip_draw(0, 0, 32, 64, self.x - start_x, self.y, 96, 192)
        elif self.type == 5:
            self.image_flag_and_flagpole.clip_draw(16, 0, 16, 152, self.x - start_x, self.y + 204, 48, 456)
        elif self.type == 6:
            self.image_horizontal_pipe_1.clip_draw(0, 0, 96, 96, self.x - start_x, self.y + 24, 96, 96)
        elif self.type == 7:
            self.image_horizontal_pipe_2.clip_draw(0, 0, 96, 480, self.x - start_x, self.y + 240-24, 96, 480)




