import game_framework
import random
from pico2d import *


star_time = 100 # 스타 지속 시간

# 각 상태 별 프레임 수
FRAME_OF_IDLE = 1;
FRAME_OF_RUN = 3;

# Mario Run Speed
# fill expressions correctly
PIXEL_PER_METER = (96.0 / 20) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# v = v_0 + at 아래 적용은 보류
TIME_TAKES_TO_ACCELARATE = 1 # 초

RUN_ACCELERATION_KMPH = 20.0 / TIME_TAKES_TO_ACCELARATE # Km / Hour
RUN_ACCELERATION_MPM = (RUN_ACCELERATION_KMPH * 1000.0 / 60.0)
RUN_ACCELERATION_MPS = (RUN_ACCELERATION_MPM / 60.0)
RUN_ACCELERATION_PPS = (RUN_ACCELERATION_MPS * PIXEL_PER_METER)


# Mario Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X_MOVE, Y_MOVE = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    # (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class IdleState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        if mario.x_speed != 0:
            mario.add_event(X_MOVE)
        if mario.y_speed != 0:
            mario.add_event(Y_MOVE)
        pass


class RunState:
    def enter(mario, event):
        mario.frame = 0 # 프레임이 2개 이상인 상태로 변환시 프레임 초기화

        if event == RIGHT_DOWN:
            mario.x_acceleration += RUN_ACCELERATION_PPS
        elif event == LEFT_DOWN:
            mario.x_acceleration -= RUN_ACCELERATION_PPS
        elif event == LEFT_DOWN:
            mario.x_acceleration -= RUN_ACCELERATION_PPS

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAME_OF_RUN


class JumpState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        # dir 만 바뀌고 속도 위치 보정
        pass


class SitState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        # 속도 감소만 한다.
        pass


class AttackState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass
# 피격 상태 추가 보류


next_state_table = {
    IdleState: {X_MOVE: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
    JumpState: {}
}


class Mario:
    def __init__(self, x = random.randint(100, 700), y=90):
        self.image = []

        self.image.append(load_image('mario_sheet_1.png'))  # 405 * 118, 16 * 6
        self.image.append(load_image('mario_sheet_2.png'))  # 405 * 118, 16 * 6
        self.image.append(load_image('mario_sheet_3.png'))  # 405 * 118, 16 * 6


        # 현재 위치
        self.x = x
        self.y = y
        # 현재 속도
        self.x_speed = 0
        self.y_speed = 0
        # 현재 가속도
        self.x_acceleration = 0
        self.y_acceleration = 0
        # 방향
        self.dir = 0 # 1 왼쪽, 0 오른쪽
        # 부울변수
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

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

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
                self.image[self.current_status].clip_draw(16 + 16*int(self.frame % 3), self.dir * 32, 16, 32, self.x, self.y, 48, 96)

        if self.star_count > 0:
            pass # 특수 효과 출력 - 별이 빙빙 도는건 어떨까

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)