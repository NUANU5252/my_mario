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
