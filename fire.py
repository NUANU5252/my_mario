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
    #0.5초에 4프레임

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

    def draw(self):
        self.image.clip_draw(8 * int(self.frame % Fire.FRAMES_PER_ACTION), self.dir * 8, 8, 8, self.x, self.y, self.x_size, self.y_size)

    def collision_with_item(self, item):
        # return 값이 ture 이면 del item
        if item.is_alive:
            if item.type == 0:
                # 상하 충돌 방향이 y 스피드 반사
                if abs(self.x - item.x) < abs(self.y - item.y):
                    self.y_speed *= -1
                # 좌우 충돌 방향이 x 스피드 반사
                else:
                    self.x_speed *= -1
                self.bounce_count += 1
                # Item_box 방향에 따라 다르다

    def del_self(self):
        print(self.bounce_count)
        print(Fire.MAX_BOUNCE_COUNT)
        print(self.bounce_count == Fire.MAX_BOUNCE_COUNT)
        game_world.remove_object(self)
        pass

    def collision_with_enemy(self, enemy):
        if enemy.is_alive:
            enemy.is_alive = False
            self.del_self()

    def crash_check(self):
        # 충돌체크
        x3 = self.x - self.x_size / 2
        x4 = self.x + self.x_size / 2
        y3 = self.y - self.y_size / 2
        y4 = self.y + self.y_size / 2

        for item in game_world.objects[2]:
            x1 = item.x - item.x_size / 2
            x2 = item.x + item.x_size / 2
            y1 = item.y - item.y_size / 2
            y2 = item.y + item.y_size / 2

            if collision_check_2(x1, y1, x2, y2, x3, y3, x4, y4):
                self.collision_with_item(item)

        for enemy in game_world.objects[1]:
            x1 = enemy.x - enemy.x_size / 2
            x2 = enemy.x + enemy.x_size / 2
            y1 = enemy.y - enemy.y_size / 2
            y2 = enemy.y + enemy.y_size / 2

            if collision_check_2(x1, y1, x2, y2, x3, y3, x4, y4):
                self.collision_with_enemy(enemy)

        # 일단 바닥 아래로 안 떨어지게 만든다.
        if self.y < 30:
            self.y = 30
            self.y_speed *= -1
            self.bounce_count += 1

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