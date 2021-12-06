# from mario_ob import *
from enemy import *
from item import *
from block import *
# from mario_ob import *
import game_world
import main_state

enemys = None
items = None
blocks = None


def choose_stage(is_bonus_stage=False):
    if not is_bonus_stage:
        if game_world.world_num == 1:
            if game_world.stage_num == 1:
                set_player_pos()
                world_1_1()
                # world_1_2()
                # bonus_area_3()
            elif game_world.stage_num == 2:
                set_player_pos(48*3, 48*10)
                world_1_2()
        else:
            # 끝 or 오류
            pass
    else:
        if game_world.world_num == 1:
            if game_world.stage_num == 1:
                bonus_area_1()
            elif game_world.stage_num == 2:
                bonus_area_2()
        else:
            # 끝 or 오류
            pass


def set_player_pos(x=48*3, y=48*2+24, start_x_=0):
    game_world.start_x = start_x_
    main_state.player.x = x
    main_state.player.y = y


def load_world(load_type=0):
    # 기본값은 클리어인 경우를 불러오는것이다. 처음 시작할때는 월드1, 스테이지0이다.
    # blocks, enenmys, items 삭제 이건 더른곳에서 하고잇음
    # game_world 삭제
    game_world.clear()

    # game_world 의 해당하는 스테이지를 불러운다.
    # 클리어 할 경우 stage 를 올리고 부른다.
    # 보너스로 가는 경우
    # 보너스에서 오는 경우
    if load_type == 0:
        # 클리어를 했으므로 stage 값을 1 증가시켜 로드를 한다.
        # stage 는 월드당 4개가 있다. 구현을 할지는 모르겠는걸
        game_world.stage_num += 1
        if game_world.stage_num == 5:
            game_world.world_num += 1
            game_world.stage_num = 1

        # set_player_pos()
        # set_player_pos(48*191, 24+48*10) # 맵의 끝 부분

        choose_stage()
    elif load_type == 1:
        # 스테이지 재 시작
        # 마리오 상태 초기화 및 목숨 감소
        main_state.player.reset_without_pos()
        # set_player_pos()

        choose_stage()
    elif load_type == 2:
        # 해당 스테이지의 보너스방을 부른다. 위에서 떨어진다.
        set_player_pos(48*3, 48*10) # y 값은 테스트 해볼걸

        choose_stage(True)
    elif load_type == 3:
        # mario_x, mario_y 가 기본값이면 오류를 발생시킨다.

        # 원래 스테이지의 특정 부븐으로 마리오를 보낸다. == 정해진 위치로
        if game_world.world_num == 1:
            if game_world.stage_num == 1:
                # blocks.append(Block(48 + 165 * 48, 48 * 2 - 24, 4))
                set_player_pos(48 * 182, 24 + 48 * 4)
            elif game_world.stage_num == 2:
                # blocks.append(Block(48 + 115 * 48, 48 * 2 - 24, 4))
                set_player_pos(48 * 116, 24 + 48 * 2)
        choose_stage()
    pass


# game_world.start_x = 0
# main_state.player.x = 48*3
# main_state.player.y = 48*2


def world_1_1(start_x_=0):
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    game_world.max_start_x = 48 * 185
    game_world.is_underground = False

    # 1층 높이값 = 5, 2층 높이값 = 9

    blocks.append(Block(24 + 17 * 48, 48 * 5, 1, [0]))

    blocks.append(Block(24 + 21 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 22 * 48, 48 * 5, 1, [1]))
    blocks.append(Block(24 + 23 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 23 * 48, 48 * 9, 1, [0]))
    blocks.append(Block(24 + 24 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 25 * 48, 48 * 5, 0))
    # 길이 2토관
    blocks.append(Block(48 + 29 * 48, 48 * 2 - 24, 4))
    # 길이 3토관
    blocks.append(Block(48 + 39 * 48, 48 * 3 - 24, 4))
    # 길이 4토관
    blocks.append(Block(48 + 47 * 48, 48 * 4 - 24, 4))
    # 길이 4토관 - 보너스 연결 토관 큐에 아무거나 넣으면 됨. 특정 값을 넣을때 다른 이벤트가 가능하게 하는것도
    blocks.append(Block(48 + 58 * 48, 48 * 4 - 24, 4, [1]))
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
    blocks.append(Block(48 + 165 * 48, 48 * 2 - 24, 4))

    blocks.append(Block(24 + 170 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 171 * 48, 48 * 5, 0))
    blocks.append(Block(24 + 172 * 48, 48 * 5, 1, [0]))
    blocks.append(Block(24 + 173 * 48, 48 * 5, 0))
    # 토관
    blocks.append(Block(48 + 181 * 48, 48 * 2 - 24, 4))
    # 깃발
    blocks.append(Block(24 + 200 * 48, 48 * 3, 5))
    blocks.append(Block(24 + 200 * 48, 48 * 2, 3))

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

    for i in range(69):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))
    for i in range(15):
        blocks.append(Block(24 + (i + 72) * 48, 0, 2))
        blocks.append(Block(24 + (i + 72) * 48, 48, 2))
    for i in range(65):
        blocks.append(Block(24 + (i + 90) * 48, 0, 2))
        blocks.append(Block(24 + (i + 90) * 48, 48, 2))
    for i in range(44):
        blocks.append(Block(24 + (i + 157) * 48, 0, 2))
        blocks.append(Block(24 + (i + 157) * 48, 48, 2))

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


def world_1_2(start_x_=0):
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    # 맵 크기 - 15 * 48
    game_world.max_start_x = 48 * (137-15)
    game_world.is_underground = True

    # 1층 높이값 = 5, 2층 높이값 = 9
    # 벽
    for i in range(11):
        blocks.append(Block(24 + 0 * 48, 0 + (i + 2) * 48, 0))
    # 천장
    for i in range(132):
        if i+6 == 89:
            blocks.append(Block(24 + (i+6) * 48, 12 * 48, 1, [1]))
        else:
            blocks.append(Block(24 + (i+6) * 48, 12 * 48, 0))

    blocks.append(Block(24 + 10 * 48, 5 * 48, 1, [1]))
    blocks.append(Block(24 + 11 * 48, 5 * 48, 1, [0]))
    blocks.append(Block(24 + 12 * 48, 5 * 48, 1, [0]))
    blocks.append(Block(24 + 13 * 48, 5 * 48, 1, [0]))
    blocks.append(Block(24 + 14 * 48, 5 * 48, 1, [0]))

    blocks.append(Block(24 + 17 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 19 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 19 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 21 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 21 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 21 * 48, 4 * 48, 3))
    blocks.append(Block(24 + 23 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 23 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 23 * 48, 4 * 48, 3))
    blocks.append(Block(24 + 23 * 48, 5 * 48, 3))
    blocks.append(Block(24 + 25 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 25 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 25 * 48, 4 * 48, 3))
    blocks.append(Block(24 + 25 * 48, 5 * 48, 3))
    blocks.append(Block(24 + 27 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 27 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 27 * 48, 4 * 48, 3))
    blocks.append(Block(24 + 29 * 48, 6 * 48, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    blocks.append(Block(24 + 31 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 31 * 48, 3 * 48, 3))
    blocks.append(Block(24 + 31 * 48, 4 * 48, 3))
    blocks.append(Block(24 + 33 * 48, 2 * 48, 3))
    blocks.append(Block(24 + 33 * 48, 3 * 48, 3))

    blocks.append(Block(24 + 39 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 39 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 39 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 40 * 48, 5 * 48, 0))
    items.append(Item(24 + 40 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 41 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 41 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 41 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 42 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 43 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 44 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 44 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 44 * 48, 7 * 48, 0))
    items.append(Item(24 + 41 * 48, 8 * 48, 0))
    items.append(Item(24 + 42 * 48, 8 * 48, 0))
    items.append(Item(24 + 43 * 48, 8 * 48, 0))
    items.append(Item(24 + 44 * 48, 8 * 48, 0))
    blocks.append(Block(24 + 45 * 48, 5 * 48, 0))
    items.append(Item(24 + 45 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 46 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 46 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 46 * 48, 7 * 48, 1, [2]))

    for i in range(5):
        blocks.append(Block(24 + 52 * 48, (5+i) * 48, 0))
        blocks.append(Block(24 + 53 * 48, (5+i) * 48, 0))
    for i in range(2):
        blocks.append(Block(24 + (54+i) * 48, 3 * 48, 0))
        blocks.append(Block(24 + (54+i) * 48, 4 * 48, 0))
        blocks.append(Block(24 + (54+i) * 48, 5 * 48, 0))
        blocks.append(Block(24 + (54+i) * 48, 10 * 48, 0))
        blocks.append(Block(24 + (54+i) * 48, 11 * 48, 0))
    for i in range(4):
        blocks.append(Block(24 + (58+i) * 48, 5 * 48, 0))
        items.append(Item(24 + (58+i) * 48, 6 * 48, 0))
        blocks.append(Block(24 + (58+i) * 48, 10 * 48, 0))
        blocks.append(Block(24 + (58+i) * 48, 11 * 48, 0))
    for i in range(7):
        blocks.append(Block(24 + 62 * 48, (5+i) * 48, 0))
        blocks.append(Block(24 + 63 * 48, (5+i) * 48, 0))

    for i in range(4):
        blocks.append(Block(24 + (66+i) * 48, 10 * 48, 0))
        blocks.append(Block(24 + (66+i) * 48, 11 * 48, 0))
    for i in range(5):
        blocks.append(Block(24 + 67 * 48, (5+i) * 48, 0))
    blocks.append(Block(24 + 68 * 48, 5 * 48, 0))
    items.append(Item(24 + 68 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 69 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 69 * 48, 6 * 48, 1, [1]))

    blocks.append(Block(24 + 72 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 72 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 72 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 72 * 48, 8 * 48, 0))
    blocks.append(Block(24 + 72 * 48, 9 * 48, 0))
    blocks.append(Block(24 + 73 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 73 * 48, 6 * 48, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    blocks.append(Block(24 + 73 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 73 * 48, 8 * 48, 0))
    blocks.append(Block(24 + 73 * 48, 9 * 48, 0))

    for i in range(4):
        blocks.append(Block(24 + (76+i) * 48, 5 * 48, 0))
        blocks.append(Block(24 + (76+i) * 48, 10 * 48, 0))
        blocks.append(Block(24 + (76+i) * 48, 11 * 48, 0))

    for i in range(6):
        blocks.append(Block(24 + (84+i) * 48, 6 * 48, 0))
        blocks.append(Block(24 + (84+i) * 48, 7 * 48, 0))
        items.append(Item(24 + (84+i) * 48, 9 * 48, 0))

    # 103 토관3 in
    blocks.append(Block(48 + 103 * 48, 48 * 3 - 24, 4, [1]))
    # 109 토관4
    blocks.append(Block(48 + 109 * 48, 48 * 4 - 24, 4))
    # 115 토관2 out
    blocks.append(Block(48 + 115 * 48, 48 * 2 - 24, 4))

    for i in range(3):
        blocks.append(Block(24 + 122 * 48, (2+i) * 48, 0))
        blocks.append(Block(24 + 123 * 48, (2+i) * 48, 0))

    for i in range(4):
        for j in range(i+1):
            blocks.append(Block(24 + (133+i) * 48, (2+j) * 48, 3))
        blocks.append(Block(24 + 137 * 48, (2+i) * 48, 3))

    # 바닥
    for i in range(80):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))

    for i in range(37):
        blocks.append(Block(24 + (i+83) * 48, 0, 2))
        blocks.append(Block(24 + (i+83) * 48, 48, 2))

    for i in range(2):
        blocks.append(Block(24 + (i + 122) * 48, 0, 2))
        blocks.append(Block(24 + (i + 122) * 48, 48, 2))

    for i in range(12):
        blocks.append(Block(24 + (i + 126) * 48, 0, 2))
        blocks.append(Block(24 + (i + 126) * 48, 48, 2))

    # 적


    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(blocks, 3)


def bonus_area_1():
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    game_world.max_start_x = 48 * 0
    game_world.is_underground = True

    for i in range(11):
        blocks.append(Block(24 + 0 * 48, 0 + (i + 2) * 48, 0))

    for i in range(7):
        blocks.append(Block(24 + (i + 4) * 48, 0 + 2 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 3 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 4 * 48, 0))
        items.append(Item(24 + (i + 4) * 48, 0 + 5 * 48, 0))
        items.append(Item(24 + (i + 4) * 48, 0 + 7 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 12 * 48, 0))

    for i in range(5):
        items.append(Item(24 + (i + 5) * 48, 0 + 9 * 48, 0))

    for i in range(16):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))

    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(blocks, 3)


def bonus_area_2():
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    game_world.max_start_x = 48 * 0
    game_world.is_underground = True

    for i in range(11):
        blocks.append(Block(24 + 0 * 48, 0 + (i + 2) * 48, 0))

    for i in range(10):
        blocks.append(Block(24 + (i + 4) * 48, 0 + 9 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 10 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 11 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 12 * 48, 0))

    for i in range(9):
        items.append(Item(24 + (i + 4) * 48, 0 + 2 * 48, 0))
        blocks.append(Block(24 + (i + 4) * 48, 0 + 5 * 48, 0))

    blocks.append(Block(24 + 13 * 48, 0 + 5 * 48, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))


    for i in range(8):
        items.append(Item(24 + (i + 5) * 48, 0 + 6 * 48, 0))

    for i in range(16):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))

    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(blocks, 3)


def bonus_area_3():
    global enemys, items, blocks
    blocks = []
    enemys = []
    items = []
    game_world.max_start_x = 48 * 0
    game_world.is_underground = True

    for i in range(11):
        blocks.append(Block(24 + 0 * 48, (i + 2) * 48, 0))

    blocks.append(Block(24 + 3 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 3 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 3 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 3 * 48, 8 * 48, 0))

    blocks.append(Block(24 + 4 * 48, 4 * 48, 0))
    items.append(Item(24 + 4 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 4 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 4 * 48, 8 * 48, 0))

    blocks.append(Block(24 + 5 * 48, 5 * 48, 0))
    items.append(Item(24 + 5 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 5 * 48, 8 * 48, 1, [1]))

    blocks.append(Block(24 + 6 * 48, 6 * 48, 0))
    items.append(Item(24 + 6 * 48, 7 * 48, 0))
    items.append(Item(24 + 6 * 48, 9 * 48, 0))

    blocks.append(Block(24 + 7 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 7 * 48, 8 * 48, 0))
    items.append(Item(24 + 7 * 48, 9 * 48, 0))
    items.append(Item(24 + 7 * 48, 10 * 48, 0))

    blocks.append(Block(24 + 8 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 8 * 48, 8 * 48, 0))
    items.append(Item(24 + 8 * 48, 9 * 48, 0))
    items.append(Item(24 + 8 * 48, 10 * 48, 0))

    blocks.append(Block(24 + 9 * 48, 6 * 48, 0))
    items.append(Item(24 + 9 * 48, 7 * 48, 0))
    items.append(Item(24 + 9 * 48, 9 * 48, 0))

    blocks.append(Block(24 + 10 * 48, 5 * 48, 0))
    items.append(Item(24 + 10 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 10 * 48, 8 * 48, 0))

    blocks.append(Block(24 + 11 * 48, 4 * 48, 0))
    items.append(Item(24 + 11 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 11 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 11 * 48, 8 * 48, 0))

    blocks.append(Block(24 + 12 * 48, 5 * 48, 0))
    blocks.append(Block(24 + 12 * 48, 6 * 48, 0))
    blocks.append(Block(24 + 12 * 48, 7 * 48, 0))
    blocks.append(Block(24 + 12 * 48, 8 * 48, 0))


    for i in range(16):
        blocks.append(Block(24 + i * 48, 0, 2))
        blocks.append(Block(24 + i * 48, 48, 2))

    game_world.add_objects(enemys, 1)
    game_world.add_objects(items, 2)
    game_world.add_objects(blocks, 3)

