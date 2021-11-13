import game_framework
import random
from pico2d import *


star_time = 100 # 스타 지속 시간

# 각 상태 별 프레임 수
FRAME_OF_IDLE = 1;
FRAME_OF_RUN = 3;

# Mario Run Speed
# fill expressions correctly
PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# v = v_0 + at 아래 적용은 보류
TIME_TAKES_TO_ACCELARATE = 0.5 # 초
TTTA = TIME_TAKES_TO_ACCELARATE
TIME_TAKES_TO_DECELERATION = 0.5 # 초
TTTD = TIME_TAKES_TO_DECELERATION

# RUN_ACCELERATION_KMPH = 20.0 / TIME_TAKES_TO_ACCELARATE # Km / Hour
# RUN_ACCELERATION_MPM = (RUN_ACCELERATION_KMPH * 1000.0 / 60.0)
# RUN_ACCELERATION_MPS = (RUN_ACCELERATION_MPM / 60.0)
RUN_ACCELERATION_PPS = RUN_SPEED_PPS / TIME_TAKES_TO_ACCELARATE


# Mario Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Mario Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X_MOVE, Y_MOVE, X_STOP, Y_STOP = range(8)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'X_MOVE', 'Y_MOVE', 'X_STOP', 'Y_STOP']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    # (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class IdleState:
    def enter(mario, event):
        # print('State: ', mario.cur_state.__name__, 'Event: ', event)
        mario.acceleration_event(event)
        pass

    def exit(mario, event):

        pass

    def do(mario):
        mario.acceleration_update()
        mario.speed_update()
        mario.dir_update()
        mario.position_update()


        if mario.x_speed != 0:
            mario.frame = 0 # 런 스테이트로 갈 때 프레임 0으로 만들어주기
            mario.add_event(X_MOVE)
        if mario.y_speed != 0:
            mario.add_event(Y_MOVE)
        pass


class RunState:
    def enter(mario, event):
        # print('State: ', mario.cur_state.__name__, 'Event: ', event_name[event])
        mario.acceleration_event(event)

    def exit(mario, event):
        pass

    def do(mario):
        mario.acceleration_update()
        mario.speed_update()
        mario.dir_update()
        mario.position_update()

        if mario.x_speed == 0:
            mario.add_event(X_STOP)
        if mario.y_speed != 0:
            mario.add_event(Y_MOVE)
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAME_OF_RUN


class JumpState:
    def enter(mario, event):
        if event == Y_MOVE:
            # y방향 가속도가 생김
            pass

    def exit(mario, event):
        if event == Y_MOVE:
            # y방향 가속도가 없어짐
            pass
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
    IdleState: {X_STOP: IdleState, X_MOVE: RunState, RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
    RunState: {X_STOP: IdleState, X_MOVE: RunState,RIGHT_UP: RunState, LEFT_UP: RunState, LEFT_DOWN: RunState, RIGHT_DOWN: RunState},
    JumpState: {}
}


class Mario:
    def __init__(self, x = random.randint(350, 450), y=90):
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

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def return_size(self):
        if self.current_status == 0:
            return 48, 48
        else:
            return 48, 96

    def acceleration_event(self, event):
        if event == RIGHT_DOWN:
            self.is_right_key_down = True
        elif event == LEFT_DOWN:
            self.is_left_key_down = True
        elif event == RIGHT_UP:
            self.is_right_key_down = False
        elif event == LEFT_UP:
            self.is_left_key_down = False

    def acceleration_update(self):
        x_acceleration = 0
        new_acceleration = RUN_ACCELERATION_PPS * game_framework.frame_time
        if self.is_right_key_down:
            x_acceleration += new_acceleration
        if self.is_left_key_down:
            x_acceleration += -new_acceleration
        self.x_acceleration = x_acceleration

    def speed_update(self, slip_coefficient=1.0):
        # 속도 설정
        # 감속
        if self.x_acceleration == 0:
            new_acceleration = (RUN_ACCELERATION_PPS * game_framework.frame_time)/ TIME_TAKES_TO_DECELERATION

            if self.x_speed > (new_acceleration / 2) * slip_coefficient:
                self.x_speed -= new_acceleration * slip_coefficient
            elif self.x_speed < -(new_acceleration / 2) * slip_coefficient:
                self.x_speed += new_acceleration * slip_coefficient
            else:
                self.x_speed = 0
        # 가속
        if (self.x_speed <= RUN_SPEED_PPS) and (self.x_speed >= -RUN_SPEED_PPS):
            if self.x_speed * self.x_acceleration < 0:
                self.x_speed += self.x_acceleration * slip_coefficient
            else:
                self.x_speed += self.x_acceleration
            self.x_speed = clamp(-RUN_SPEED_PPS, self.x_speed, RUN_SPEED_PPS)

    def position_update(self):
        self.x += self.x_speed * game_framework.frame_time
        self.y += self.y_speed * game_framework.frame_time
        self.x = clamp(25, self.x, 800 - 25)

    def dir_update(self):
        if self.x_acceleration > 0:
            self.dir = 0
        elif self.x_acceleration < 0:
            self.dir = 1

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

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                # 일단 아래 문장을 실행해보기
                self.cur_state = next_state_table[self.cur_state][event]
            except:
            #     만약 문제가 있으면, 아래를 실행
            #   어떤 정보가 필요??? 현재 상태 정보, 이벤트의 종류
                print('State: ', self.cur_state.__name__, 'Event: ', event_name[event])
                exit(-1) # 강제 종료
                pass
            self.cur_state.enter(self, event)
            # self.cur_state = next_state_table[self.cur_state][event]
            # self.cur_state.enter(self, event)

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
        # print(event.type, event.key)
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)