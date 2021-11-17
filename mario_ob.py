import random
import mario
from pico2d import *

class Grass:
    def __init__(self): # 생성자
        self.image = load_image('sheet/grass.png')
        self.x = 400
        self.y = 30

    def draw(self):
        self.image.draw(400, 30)

    def get_bb(self):
        return self.x - 400, self.y - 30, self.x + 400, self.y + 30

    def update(self):
        pass


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

        self.x = x
        self.y = y
        self.frame_delay = 0
        self.frame = 0
        self.is_alive = True

    def get_bb(self):
        if self.type == 1:
            return self.x - 12, self.y - 24, self.x + 12, self.y + 24
        else:
            return self.x - 24, self.y - 24, self.x + 24, self.y + 24

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