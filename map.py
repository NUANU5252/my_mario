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
    # enemys.append(Enemy(x=50))
    enemys.append(Enemy(x=600, type=1))

    for i in range(20):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))
        if i > 10:
            for j in range(i - 9):
                blocks.append(Block(24 + i * 48, 48 + j * 48, 2))

    blocks.append(Block(24 + 3 * 48, 48 + 4 * 48, 0, [1, 1]))
    blocks.append(Block(24 + 5 * 48, 48 + 4 * 48, 1, [1, 1, 2]))


    game_world.add_objects(blocks, 3)
    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)

