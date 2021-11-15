import random
import mario
from pico2d import *

star_time = 100 # 스타 지속 시간


class Grass:
    def __init__(self): # 생성자
        self.image = load_image('sheet/grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass






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
            self.image = Enemy.image_1 #
        elif type == 1:
            self.image = Enemy.image_2 #
        self.x = x
        self.y = y
        # 사이즈
        self.x_size = 48
        if type == 0:
            self.y_size = 48
        elif type == 1:
            self.y_size = 72
        # 현재 속도
        self.x_speed = 5
        self.y_speed = 0

        self.dir = 0 # 우, 좌
        self.dir_count = 0

        self.is_alive = True

        self.frame = 0

    def AI_update(self):
        # AI 작성
        if self.dir_count > 10:
            self.dir = (self.dir + 1) % 2
            self.dir_count = 0
        self.dir_count += 1
        if self.dir == 0:
            self.x += self.x_speed
        else:
            self.x += -self.x_speed

    def update(self):
        if self.is_alive:
            self.AI_update()

        if (self.dir_count % 2) == 0:
            self.frame = (self.frame + 1) % 4

    def draw(self):
        if not self.is_alive: # 사망
            self.image.clip_draw(16 * 4, self.dir * 32, 16, 32, self.x, self.y, 48, 96) # 3배수 출력
        else:
            self.image.clip_draw(self.frame*16, self.dir*32, 16, 32, self.x, self.y, 48, 96)


class Item:
    image_box = None
    image_coin = None
    image_power = None
    image_star = None

    def __init__(self, x=random.randint(50, 750), y=random.randint(140, 550), type=0):
        self.type = type
        if Item.image_box == None:
            Item.image_box = load_image('sheet/items_sheet_box.png')
        if Item.image_coin == None:
            Item.image_coin = load_image('sheet/items_sheet_coin.png')
        if Item.image_power == None:
            Item.image_power = load_image('sheet/items_sheet_power.png')
        if Item.image_star == None:
            Item.image_star = load_image('sheet/items_sheet_star.png')

        # 이미지
        if type == 0:
            self.image = Item.image_box
        if type == 1:
            self.image = Item.image_coin
        if type == 2:
            self.image = Item.image_power
        if type == 3:
            self.image = Item.image_star

        # 사이즈
        if type == 1:
            self.x_size = 24
        else:
            self.x_size = 48
        self.y_size = 48

        self.x = x
        self.y = y
        self.frame_delay = 0
        self.frame = 0
        self.is_alive = True

    def update(self):
        if self.frame_delay % 2 == 0:
            if self.type == 0:
                self.frame = (self.frame + 1) % 4
            elif self.type == 1:
                self.frame = (self.frame + 1) % 8
            elif self.type == 2 or self.type == 3:
                self.frame = (self.frame + 1) % 6
        self.frame_delay += 1

    def draw(self, player_status=0):
        if self.is_alive:
            if self.type == 1:
                self.image.clip_draw(8 * self.frame, 0, 8, 16, self.x, self.y, 24, 48) # 3배수 출력
            elif self.type == 2:
                if player_status == 0:
                    y_frame = 1
                else:
                    y_frame = 0
                self.image.clip_draw(16 * self.frame, y_frame*16, 16, 16, self.x, self.y, 48, 48)
            else:
                self.image.clip_draw(self.frame*16, 0, 16, 16, self.x, self.y, 48, 48)

    def __del__(self):
        pass