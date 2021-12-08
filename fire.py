from pico2d import *
from crash_check import *
import game_framework
import game_world


PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_TAKES_TO_ACCELARATE = 0.3 # 초
Gravitational_acceleration_MPS = 10 / TIME_TAKES_TO_ACCELARATE# m/s
Gravitational_acceleration_PPS = Gravitational_acceleration_MPS * PIXEL_PER_METER

class Fire:
    TIME_PER_ACTION = 0.1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    MAX_BOUNCE_COUNT = 3
    #0.1초에 4프레임

    def __init__(self, x, y, dir): # 생성자
        self.image = load_image('sheet/fire_sheet.png')
        self.y = y
        self.x_size = 16
        self.y_size = 16

        self.live_time = 2
        self.bounce_count = 0

        self.dir = dir# 1 왼쪽, 0 오른쪽
        if self.dir == 0:
            self.x_speed = RUN_SPEED_PPS
            self.x = x + 24 + 8  # 마리오 크기의 절반 + 자신 크기의 절반 마리오는 16*3, 불은 8*2
        elif self.dir == 1:
            self.x_speed = -RUN_SPEED_PPS
            self.x = x - (24 + 8)  # 마리오 크기의 절반 + 자신 크기의 절반 마리오는 16*3, 불은 8*2


        self.y_speed = 0
        self.frame = 0

    def draw(self, start_x=0):
        self.image.clip_draw(8 * int(self.frame % Fire.FRAMES_PER_ACTION), self.dir * 8, 8, 8, self.x - start_x, self.y, self.x_size, self.y_size)

    def collision_with_block(self, block):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = block.get_bb()

        col_dir = collide_direction(self, block)
        print(col_dir)
        if col_dir == 2:
            self.y -= top_a - bottom_b - 1
        elif col_dir == 6:
            self.x += right_b - left_a
        elif col_dir == 4:
            self.x -= right_a - left_b
        elif col_dir == 8:
            self.y += top_b - bottom_a + 1
        elif col_dir == 5:
            pass

        # 상하 충돌 방향이 y 스피드 초기화
        if abs(self.x - block.x) < abs(self.y - block.y):
            self.y_speed = RUN_SPEED_PPS * 1.5
        # 좌우 충돌 방향이 x 스피드 반사
        else:
            self.x_speed *= -1
        self.bounce_count += 1

    def del_self(self):
        print(self.bounce_count)
        print(Fire.MAX_BOUNCE_COUNT)
        print(self.bounce_count == Fire.MAX_BOUNCE_COUNT)
        game_world.remove_object(self)
        pass

    def get_bb(self , start_x=0):
        return self.x - 8 - start_x, self.y - 8, self.x + 8 - start_x, self.y + 8

    def collision_with_enemy(self, enemy):
        if enemy.is_alive:
            enemy.del_event()
            self.del_self()

    def crash_check(self):
        # 충돌체크
        for block in game_world.objects[3]:
            if collide(self, block):
                self.collision_with_block(block)

        for enemy in game_world.objects[1]:
            if collide(self, enemy):
                self.collision_with_enemy(enemy)

    def update(self):
        if self.x_speed > 0:
            self.dir = 0
        else:
            self.dir = 1

        if self.live_time > 0:
            self.live_time -= game_framework.frame_time
        elif self.live_time <= 0:
            self.del_self()

        if self.bounce_count == Fire.MAX_BOUNCE_COUNT:
            self.del_self()

        # 중력가속도
        self.y_speed -= Gravitational_acceleration_PPS * game_framework.frame_time
        # 위치 변경
        self.x += self.x_speed * game_framework.frame_time
        self.y += self.y_speed * game_framework.frame_time
        # 충돌체크
        self.crash_check()

        self.frame = (self.frame + Fire.FRAMES_PER_ACTION * Fire.ACTION_PER_TIME * game_framework.frame_time) % Fire.FRAMES_PER_ACTION
        pass