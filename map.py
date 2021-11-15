from mario_ob import *
import game_world

enemys = None
items = None
grass = None

def world_1_1():
    global enemys, items, grass

    enemys = []
    items = []
    enemys.append(Enemy(x=50))
    enemys.append(Enemy(x=600, type=1))

    for i in range(4):
        items.append(Item(x=100 + 100 * i, y=250, type=i))

    items.append(Item(x=100 + 100 * i, y=150, type=2))

    grass = Grass()
    game_world.add_object(grass, 0)
    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)

