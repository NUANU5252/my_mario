from mario_ob import *
from enemy import *
from item import *
from block import *
from mario_ob import *
import game_world

enemys = None
items = None
blocks = None

def world_1_1():
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    enemys.append(Enemy(x=50))
    enemys.append(Enemy(x=600, type=1))

    for i in range(3):
        items.append(Item(x=100 + 100 * i, y=250, type=i))

    items.append(Item(x=100 + 100 * i, y=150, type=1))

    for i in range(20):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))
        if i > 10:
            for j in range(i - 9):
                blocks.append(Block(24 + i * 48, 48 + j * 48, 2))

    blocks.append(Block(24 + 4 * 48, 48 + 3 * 48, 0, [1, 1]))


    game_world.add_objects(blocks, 3)
    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)

