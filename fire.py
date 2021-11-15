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
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    #0.5초에 4프레임

    def __init__(self, x, y): # 생성자
        self.image = load_image('sheet/fire_sheet.png')
        self.x = x + 24 + 8 # 마리오 크기의 절반 + 자신 크기의 절반 마리오는 16*3, 불은 8*2
        self.y = y
        self.x_size = 16
        self.y_size = 16
        self.live_time = 2
        self.x_speed
        self.y_speed

    def draw(self):
        self.image.draw(400, 30)
        self.image.clip_draw(8 * int(self.frame % Fire.FRAMES_PER_ACTION), 0, 8, 8, self.x, self.y, self.x_size, self.y_size)

    def collision_with_item(self, item):
        # return 값이 ture 이면 del item
        if item.is_alive:
            if item.type == 0:
                # 상하 충돌 방향이 y 스피드 반사
                # 좌우 충돌 방향이 x 스피드 반사
                pass
                # Item_box 방향에 따라 다르다

    def collision_with_enemy(self, enemy, invincible_time=2):
        # return 값이 ture 이면 del item
        if enemy.is_alive:
            if True: # 방향에 따라서
                if self.star_count == 0: # 무적이 아니면
                    self.change_status(False)
                    self.star_count = invincible_time * 12

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

    def update(self):
        # 중력가속도
        self.y_speed -= Gravitational_acceleration_PPS * game_framework.frame_time
        # 위치 변경
        self.x += self.x_speed * game_framework.frame_time
        self.y += self.y_speed * game_framework.frame_time
        # 충돌체크


        self.frame = (self.frame + Fire.FRAMES_PER_ACTION * Fire.ACTION_PER_TIME * game_framework.frame_time) % Fire.FRAMES_PER_ACTION
        pass