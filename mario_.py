import game_framework
import random
from pico2d import *


star_time = 100 # 스타 지속 시간

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (96.0 / 20) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Mario:
    image_1 = None
    image_2 = None
    image_3 = None

    def __init__(self, x = random.randint(100, 700), y = 90):
        if Mario.image_1 == None:
            Mario.image_1 = load_image('mario_sheet_1.png')
        if Mario.image_2 == None:
            Mario.image_2 = load_image('mario_sheet_2.png')
        if Mario.image_3 == None:
            Mario.image_3 = load_image('mario_sheet_3.png')

        self.image = []
        self.image.append(Mario.image_1)  # 405 * 118, 16 * 6
        self.image.append(Mario.image_2)  # 405 * 118, 16 * 6
        self.image.append(Mario.image_3)  # 405 * 118, 16 * 6
        # 현재 위치
        self.x = x
        self.y = y
        # 현재 속도
        self.x_speed = 0
        self.y_speed = 0
        # 현재 가속도
        self.x_acceleration = 0
        self.y_acceleration = 0

        self.dir = 0 # 1 왼쪽, 0 오른쪽

        self.is_jumping = False
        self.is_sit_down = False
        self.is_alive = True
        self.is_attacking = False
        self.is_changing_status = False
        self.is_on_flag = False
        # self.is_turning = False # 보류 == x_speed * x_acceleration < 0

        self.is_right_key_down = False
        self.is_left_key_down = False
        self.is_up_key_down = False     # 점프
        self.jump_count = 0             # 점프했을때 y_speed가 더해질 수 있는 횟수

        self.star_count = 0 # 1이상이면 무적
        self.status_count = 0
        self.attack_count = 0
        self.attack_cool_time = 0

        self.current_status = 0 # 0 : 기본, 1 : 버섯, 2 : 꽃
        self.now_status = None
        self.later_status = None

        self.frame = 0

    def change_status(self, is_upgrade=True):
        if not self.is_changing_status:
            self.is_changing_status = True

            self.now_status = self.current_status
            if is_upgrade:
                # 점수 get
                if self.current_status < 2:
                    self.later_status = self.current_status + 1
                else:
                    self.is_changing_status = False
            elif not is_upgrade:
                if self.current_status == 0:
                    self.is_alive = False
                    self.die()
                elif self.current_status < 3:
                    self.later_status = self.current_status - 1

    def attack(self): #
        if not self.is_jumping and not self.is_sit_down and self.current_status == 2:
            self.is_attacking = True
            self.attack_count = 5
            self.attack_cool_time = self.attack_count + 2

    def attack_update(self):
        if self.attack_cool_time > 0:
            if self.attack_count == 0:
                self.is_attacking = False
            self.attack_count += -1
            self.attack_cool_time += -1

    def status_update(self):
        if (self.status_count % 2) == 0:
            self.current_status = self.now_status
        elif (self.status_count % 2) == 1:
            self.current_status = self.later_status
        self.status_count += 1
        if self.status_count == 12:
            self.is_changing_status = False
            self.status_count = 0
            self.now_status = None
            self.later_status = None

    def acceleration_update(self):
        x_acceleration = 0
        if self.is_right_key_down:
            x_acceleration += 1
        if self.is_left_key_down:
            x_acceleration += -1
        self.x_acceleration = x_acceleration

    def speed_update(self):
        if self.is_jumping:
            self.y_acceleration = -2

        if not self.is_jumping:
            # 감속
            if not self.is_sit_down:
                if self.x_acceleration == 0:
                    if self.x_speed > 0.5:
                        self.x_speed += -1
                    elif self.x_speed < -0.5:
                        self.x_speed += 1
                    else:
                        self.x_speed = 0
            elif self.is_sit_down:
                if self.x_acceleration == 0:
                    if self.x_speed > 0.25:
                        self.x_speed += -0.5
                    elif self.x_speed < -0.25:
                        self.x_speed += 0.5
                    else:
                        self.x_speed = 0
            # 가속
            if (self.x_speed <= 10) and (self.x_speed >= -10):
                self.x_speed += self.x_acceleration
                if self.x_speed > 10:  # 없으면 마리오가 철산고를 사용한다.@@@@@@@
                    self.x_speed = 10
                if self.x_speed < -10:
                    self.x_speed = -10  # @@@@@@@@
        self.y_speed += self.y_acceleration

    def get_star(self, time=star_time): #
        self.star_count = time

    def on_flag(self):
        pass # 충돌과 깃발 만들면 작성

    def die(self):
        self.x_speed = 0
        self.x_acceleration = 0
        self.y_speed = 20
        self.y_acceleration = -2
        self.is_jumping = False

    def update(self):
        # 공격 쿨다운
        self.attack_update()
        # 무적시간 쿨다운
        if self.star_count > 0:
            self.star_count -= 1

        if not self.is_alive:
            self.y_speed += self.y_acceleration
            self.y += self.y_speed
        if self.is_on_flag:
            self.on_flag()
        # 변화 상태인지 확인 - 이때 모든 행동이 멈춘다.
        elif self.is_changing_status and self.is_alive:
            self.status_update()
        elif not self.is_changing_status:
            # 키 입력 확인
            # 가속도 설정
            self.acceleration_update()

            # 점프 설정
            if self.is_up_key_down:
                if self.jump_count < 5:
                    self.is_jumping = True
                    self.y_speed += 10 - self.jump_count * 2
                    self.jump_count += 1

            # 방향 설정
            if self.x_acceleration > 0:
                self.dir = 0
            elif self.x_acceleration < 0:
                self.dir = 1
            # 속도 설정 - 원상 복귀
            self.speed_update()

            # 위치 설정
            self.x += self.x_speed
            self.y += self.y_speed

            if self.y < 90 and self.is_jumping:
                self.is_jumping = False
                self.y = 90
                self.y_acceleration = 0
                self.y_speed = 0
                self.jump_count = 0

            self.frame += 1

    def return_size(self):
        if self.current_status == 0:
            return 48, 48
        else:
            return 48, 96

    def collision_with_item(self, item):
        # return 값이 ture 이면 del item
        if item.is_alive:
            if item.type == 0:
                pass
                # Item_box 방향에 따라 다르다
            elif item.type == 1:
                pass
                # Item_coin
            elif item.type == 2:
                self.change_status()
                item.is_alive = False
                return True
                # Item_power
            elif item.type == 3:
                pass
                # Item_star

    def collision_with_enemy(self, enemy):
        # return 값이 ture 이면 del item
        if enemy.is_alive:
            if True: # 방향에 따라서
                if self.star_count == 0: # 무적이 아니면
                    self.change_status(False)
                    self.star_count = 48 # 적당한 값 필요 일단 12의 배수로

    def draw(self):
        if self.star_count % 2 == 0:
            if not self.is_alive: # 사망
                self.image[0].clip_draw(16 * 6, self.dir * 32, 16, 32, self.x, self.y, 48, 96) # 3배수 출력
            elif self.is_jumping: # 점프
                self.image[self.current_status].clip_draw(16 * 5, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.is_sit_down and self.current_status != 0: # 앉기
                self.image[self.current_status].clip_draw(16 * 6, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.is_attacking and self.current_status == 2: # 공격
                self.image[self.current_status].clip_draw(16 * 7, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.x_speed == 0: # 기본
                self.image[self.current_status].clip_draw(0, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.x_speed * self.x_acceleration < 0: # 철산고 방향전환
                self.image[self.current_status].clip_draw(16 * 4, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            else: # 이동
                self.image[self.current_status].clip_draw(16 + 16*(self.frame % 3), self.dir * 32, 16, 32, self.x, self.y, 48, 96)

        if self.star_count > 0:
            pass # 특수 효과 출력 - 별이 빙빙 도는건 어떨까