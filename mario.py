import game_framework
import random
import game_world
from pico2d import *
from crash_check import *
from fire import *


star_time = 100 # 스타 지속 시간

# 각 상태 별 프레임 수는 각 상태의 클라스에 정의

# Mario Run Speed
# fill expressions correctly
PIXEL_PER_METER = (96.0 / 2) # 96 pixel 200 cm or 140 ~ 180
RUN_SPEED_KMPH = 20.0 # Km / Hour = 최대치
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# v = v_0 + at 아래 적용은 보류
TIME_TAKES_TO_ACCELARATE = 0.3 # 초
TTTA = TIME_TAKES_TO_ACCELARATE
TIME_TAKES_TO_DECELERATION = 0.5 # 초
TTTD = TIME_TAKES_TO_DECELERATION

# RUN_ACCELERATION_KMPH = 20.0 / TIME_TAKES_TO_ACCELARATE # Km / Hour
# RUN_ACCELERATION_MPM = (RUN_ACCELERATION_KMPH * 1000.0 / 60.0)
# RUN_ACCELERATION_MPS = (RUN_ACCELERATION_MPM / 60.0)
RUN_ACCELERATION_PPS = RUN_SPEED_PPS / TIME_TAKES_TO_ACCELARATE

Gravitational_acceleration_MPS = 10 / TIME_TAKES_TO_ACCELARATE# m/s
Gravitational_acceleration_PPS = Gravitational_acceleration_MPS * PIXEL_PER_METER

# Mario Event
RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, SPACE_DOWN,\
RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, \
X_MOVE, Y_MOVE, X_STOP, Y_STOP, ATTACK_OVER = range(14)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'UP_DOWN', 'DOWN_DOWN', 'SPACE_DOWN',
              'RIGHT_UP', 'LEFT_UP', 'UP_UP', 'DOWN_UP',
              'X_MOVE', 'Y_MOVE', 'X_STOP', 'Y_STOP', 'ATTACK_OVER']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,

    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,

    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN
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
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

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
            mario.frame = 0
            mario.add_event(X_STOP)
        else:
            RunState.TIME_PER_ACTION = RUN_SPEED_PPS / (mario.x_speed * 1)
            RunState.ACTION_PER_TIME = 1.0 / RunState.TIME_PER_ACTION
            mario.frame = (mario.frame + RunState.FRAMES_PER_ACTION * RunState.ACTION_PER_TIME * game_framework.frame_time) % RunState.FRAMES_PER_ACTION
        if mario.y_speed != 0:
            mario.add_event(Y_MOVE)


class JumpState:
    jump_time = 0.3 # 상승 시간
    additional_jump_time = jump_time / 2 # 높이가 추가로 증가하는 시간
    jump_height = Gravitational_acceleration_PPS * jump_time * jump_time / 2
    def enter(mario, event):
        if event == UP_DOWN:
            if mario.is_jumping == False:
                mario.jump_count = JumpState.additional_jump_time
                # mario.y_speed = JumpState.jump_height * 2 / JumpState.jump_time
                mario.y_speed = Gravitational_acceleration_PPS * JumpState.jump_time
                mario.is_jumping = True

        else:
            mario.acceleration_event(event)

    def exit(mario, event):

        if event == UP_UP:
            mario.jump_count = 0;
            # y방향 가속도가 없어짐
            pass
        pass

    def do(mario):
        mario.acceleration_update()
        mario.y_acceleration_update()
        # mario.speed_update()
        mario.y_speed_update()
        # 카운트를 센다 일정 시간동안만 속도를 더한다.
        mario.dir_update()
        mario.position_update()

        # 충돌하면 조건에 따라서 이벤트 발생
        mario.jump_update()
        pass


class SitState:
    def enter(mario, event):
        mario.acceleration_event(event)
        mario.is_sit_down = True
        pass

    def exit(mario, event):
        mario.is_sit_down = False
        pass

    def do(mario):
        mario.acceleration_update()
        mario.speed_update(0.5)
        mario.position_update()

        pass


class AttackState:
    def enter(mario, event):
        mario.acceleration_event(event)

        if event == SPACE_DOWN and mario.is_attacking == False:
            if mario.current_status == 2:
                mario.is_attacking = True
                mario.attack_count = 0.5
                mario.fire()
            else:
                pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.attack_count -= game_framework.frame_time
        if mario.attack_count < 0:
            mario.is_attacking = False
            mario.add_event(ATTACK_OVER)
        pass
# 피격 상태 추가 보류


next_state_table = {
    IdleState: {X_STOP: IdleState, X_MOVE: RunState, Y_STOP: IdleState,
                RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState,
                LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, UP_DOWN: JumpState, DOWN_DOWN: SitState, SPACE_DOWN: AttackState
                },
    RunState: {X_STOP: IdleState, X_MOVE: RunState,
               RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP: RunState, DOWN_UP: RunState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState, UP_DOWN: JumpState, DOWN_DOWN: SitState, SPACE_DOWN: AttackState
               },
    JumpState: {Y_STOP: IdleState,
                RIGHT_UP: JumpState, LEFT_UP: JumpState, UP_UP: JumpState, DOWN_UP: JumpState,
                LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, UP_DOWN: JumpState, DOWN_DOWN: JumpState, SPACE_DOWN: JumpState
                },
    SitState: {
                RIGHT_UP: SitState, LEFT_UP: SitState, UP_UP: SitState, DOWN_UP: IdleState,
                LEFT_DOWN: SitState, RIGHT_DOWN: SitState, UP_DOWN: JumpState, DOWN_DOWN: SitState, SPACE_DOWN: SitState
    },
    AttackState: {ATTACK_OVER: IdleState, X_MOVE: AttackState,
                  RIGHT_UP: AttackState, LEFT_UP: AttackState, UP_UP: AttackState, DOWN_UP: AttackState,
                  LEFT_DOWN: AttackState, RIGHT_DOWN: AttackState, UP_DOWN: AttackState, DOWN_DOWN: AttackState, SPACE_DOWN: AttackState,
                  }
}


class Mario:
    def __init__(self, x = random.randint(350, 450), y=90):
        self.image = []

        self.image.append(load_image('sheet/mario_sheet_1.png'))  # 405 * 118, 16 * 6
        self.image.append(load_image('sheet/mario_sheet_2.png'))  # 405 * 118, 16 * 6
        self.image.append(load_image('sheet/mario_sheet_3.png'))  # 405 * 118, 16 * 6


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

    def fire(self):
        fire = Fire(self.x, self.y, self.dir)
        game_world.add_object(fire, 3)

    def die(self):
        # 수정 필요
        self.x_speed = 0
        self.x_acceleration = 0
        self.y_speed = 20
        self.y_acceleration = -2
        self.is_jumping = False

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

    def status_update(self, update_time=0.5, update_frame=12):
        if (int(self.status_count) % 2) == 0:
            self.current_status = self.now_status
        elif (int(self.status_count) % 2) == 1:
            self.current_status = self.later_status
        self.status_count += 1 / update_time * update_frame * game_framework.frame_time
        if self.status_count >= update_frame:
            self.is_changing_status = False
            self.status_count = 0
            self.now_status = None
            self.later_status = None

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

    def collision_with_enemy(self, enemy, invincible_time=2):
        # return 값이 ture 이면 del item
        if enemy.is_alive:
            if True: # 방향에 따라서
                if self.star_count == 0: # 무적이 아니면
                    self.change_status(False)
                    self.star_count = invincible_time * 12

    def crash_check(self):
        # 충돌체크
        player_x_size, player_y_size = self.return_size()
        x3 = self.x - player_x_size / 2
        x4 = self.x + player_x_size / 2
        y3 = self.y - player_y_size / 2
        y4 = self.y + player_y_size / 2

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
        pass

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
        
    def y_acceleration_update(self):
        y_acceleration = 0
        new_acceleration = -Gravitational_acceleration_PPS * game_framework.frame_time
        if self.cur_state == JumpState:
            y_acceleration += new_acceleration
        self.y_acceleration = y_acceleration

    def speed_update(self, slip_coefficient=1.0):
        # 속도 설정
        # 감속
        if self.x_acceleration == 0: # and self.cur_state != JumpState
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
    
    def y_speed_update(self):
        if self.jump_count > 0:
            self.jump_count -= game_framework.frame_time
        else:
            self.y_speed += self.y_acceleration

    def jump_update(self):
        if self.y < 90 and self.cur_state == JumpState:
            self.y = 90
            self.y_acceleration = 0
            self.y_speed = 0
            self.jump_count = 0
            self.is_jumping = False
            self.add_event(Y_STOP)

    def position_update(self):
        self.x += self.x_speed * game_framework.frame_time
        self.y += self.y_speed * game_framework.frame_time
        self.x = clamp(25, self.x, 800 - 25)

    def dir_update(self):
        if self.x_acceleration > 0:
            self.dir = 0
        elif self.x_acceleration < 0:
            self.dir = 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if not self.is_alive:
            self.y_speed += self.y_acceleration * game_framework.frame_time
            self.y += self.y_speed
        elif self.is_changing_status:
            self.status_update()
        else:
            self.star_count -= 12 * game_framework.frame_time
            if self.star_count < 0:
                self.star_count = 0

            self.crash_check()
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
        if int(self.star_count % 2) == 0:
            if not self.is_alive: # 사망
                self.image[0].clip_draw(16 * 9, self.dir * 32, 16, 32, self.x, self.y, 48, 96) # 3배수 출력
            elif self.is_jumping: # 점프
                self.image[self.current_status].clip_draw(16 * 8, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.is_sit_down and self.current_status != 0: # 앉기
                self.image[self.current_status].clip_draw(16 * 9, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.is_attacking and self.current_status == 2: # 공격
                self.image[self.current_status].clip_draw(16 * 10, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.x_speed == 0: # 기본
                self.image[self.current_status].clip_draw(0, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            elif self.x_speed * self.x_acceleration < 0: # 철산고 방향전환
                self.image[self.current_status].clip_draw(16 * 7, self.dir * 32, 16, 32, self.x, self.y, 48, 96)
            else: # 이동
                self.image[self.current_status].clip_draw(16 + 16*int(self.frame % 6), self.dir * 32, 16, 32, self.x, self.y, 48, 96)

        if self.star_count > 0:
            pass # 특수 효과 출력 - 별이 빙빙 도는건 어떨까

    def handle_event(self, event):
        # print(event.type, event.key)
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)