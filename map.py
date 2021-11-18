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
    # 1층 높이값 = 5, 2층 높이값 = 9
    for i in range(69):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))
    for i in range(15):
        blocks.append(Block(24 + (i + 72) * 48, 0, 2))
        blocks.append(Block(24 + (i + 72) * 48, 48, 2))
    for i in range(65):
        blocks.append(Block(24 + (i + 90) * 48, 0, 2))
        blocks.append(Block(24 + (i + 90) * 48, 48, 2))
    for i in range(42):
        blocks.append(Block(24 + (i + 157) * 48, 0, 2))
        blocks.append(Block(24 + (i + 157) * 48, 48, 2))

    blocks.append(Block(24 + 17 * 48, 48 * 5, 1, [0]))

    blocks.append(Block(24 + 21 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 22 * 48, 48 * 5, 1, [1]))
    blocks.append(Block(24 + 23 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 23 * 48, 48 * 9, 1, [0]))
    blocks.append(Block(24 + 24 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 25 * 48, 48 * 5, 0))
    # 길이 2토관
    blocks.append(Block(24 + 29 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 29 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 30 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 30 * 48, 48 * 3, 3))
    # 길이 3토관
    blocks.append(Block(24 + 39 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 39 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 39 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 40 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 40 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 40 * 48, 48 * 4, 3))
    # 길이 4토관
    blocks.append(Block(24 + 47 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 47 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 47 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 47 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 48 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 48 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 48 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 48 * 48, 48 * 5, 3))
    # 길이 4토관
    blocks.append(Block(24 + 58 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 58 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 58 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 58 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 59 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 59 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 59 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 59 * 48, 48 * 5, 3))
    # 버섯
    blocks.append(Block(24 + 65 * 48, 48 * 5, 1, [1]))

    blocks.append(Block(24 + 78 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 79 * 48, 48 * 5, 1, [1]))
    blocks.append(Block(24 + 80 * 48, 48 * 5, 0))

    blocks.append(Block(24 + 81 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 82 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 83 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 84 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 85 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 86 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 87 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 88 * 48, 48 * 9, 0))

    blocks.append(Block(24 + 92 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 93 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 94 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 95 * 48, 48 * 9, 1, [0]))
    blocks.append(Block(24 + 95 * 48, 48 * 5, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

    blocks.append(Block(24 + 101 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 102 * 48, 48 * 5, 1, [2]))

    blocks.append(Block(24 + 107 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 110 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 110 * 48, 48 * 9, 1, [1]))
    blocks.append(Block(24 + 113 * 48, 48 * 5, 1, [0]))

    blocks.append(Block(24 + 119 * 48, 48 * 5, 0))
    # 여기부터 잘 못 카운트 한 것 같음
    blocks.append(Block(24 + 122 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 123 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 124 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 125 * 48, 48 * 9, 0))

    blocks.append(Block(24 + 130 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 131 * 48, 48 * 9, 1, [0]))
    blocks.append(Block(24 + 132 * 48, 48 * 9, 1, [0]))
    blocks.append(Block(24 + 133 * 48, 48 * 9, 0))
    blocks.append(Block(24 + 131 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 132 * 48, 48 * 5, 0))
    # 계단
    for i in range(4 + 1):
        for j in range(i):
            blocks.append(Block(24 + (135 + i) * 48, 48 * (2 + j), 3))

    # 계단
    blocks.append(Block(24 + 142 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 142 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 142 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 142 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 143 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 143 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 143 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 144 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 144 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 145 * 48, 48 * 2, 3))

    # 계단
    blocks.append(Block(24 + 150 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 151 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 151 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 152 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 152 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 152 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 153 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 153 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 153 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 153 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 154 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 154 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 154 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 154 * 48, 48 * 5, 3))
    # 계단
    blocks.append(Block(24 + 157 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 157 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 157 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 157 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 158 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 158 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 158 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 159 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 159 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 160 * 48, 48 * 2, 3))
    # 토관
    blocks.append(Block(24 + 165 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 165 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 166 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 166 * 48, 48 * 3, 3))

    blocks.append(Block(24 + 170 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 171 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 172 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 173 * 48, 48 * 5, 0))
    # 토관
    blocks.append(Block(24 + 181 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 181 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 182 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 182 * 48, 48 * 3, 3))
    # 계단
    for i in range(8 + 1):
        for j in range(i):
            blocks.append(Block(24 + (182 + i) * 48, 48 * (2 + j), 3))
    blocks.append(Block(24 + 191 * 48, 48 * 2, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 3, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 4, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 5, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 6, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 7, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 8, 3))
    blocks.append(Block(24 + 191 * 48, 48 * 9, 3))

    enemys.append(Enemy(24 + 21 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 41 * 48, 48 * 2, 0))

    enemys.append(Enemy(24 + 54 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 55 * 48, 48 * 2, 0))

    enemys.append(Enemy(24 + 81 * 48, 48 * 10, 0))
    enemys.append(Enemy(24 + 83 * 48, 48 * 10, 0))

    enemys.append(Enemy(24 + 96 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 97 * 48, 48 * 2, 0))

    enemys.append(Enemy(24 + 107 * 48, 48 * 2, 1))

    enemys.append(Enemy(24 + 125 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 126 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 128 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 129 * 48, 48 * 2, 0))

    enemys.append(Enemy(24 + 175 * 48, 48 * 2, 0))
    enemys.append(Enemy(24 + 176 * 48, 48 * 2, 0))

    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(blocks, 3)

