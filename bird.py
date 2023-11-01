# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework

# state event check
# ( state event type, event value )

# def right_down(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
#
#
# def right_up(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
#
#
# def left_down(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
#
#
# def left_up(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
#
# def space_down(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
#
# def time_out(e):
#     return e[0] == 'TIME_OUT'
#
# # time_out = lambda e : e[0] == 'TIME_OUT'




# bird Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0   # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

# bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Fly:
    @staticmethod
    def enter(bird, e):
        bird.dir = 1
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        if bird.x >= 1600-25:
            bird.dir = -1
        elif bird.x <= 25:
            bird.dir = 1
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        bird.x = clamp(25, bird.x, 1600-25)

        if int(bird.frame) <= 4:
            bird.action = 2
        elif int(bird.frame) > 4 and int(bird.frame) <= 9:
            bird.action = 1
        elif int(bird.frame) > 9 and int(bird.frame) <= 13:
            bird.action = 0
            if int(bird.frame) == 13:
                bird.frame = 0
                bird.action = 2

    @staticmethod
    def draw(bird):
        if bird.dir > 0:
            bird.image.clip_draw(int(bird.frame%5) * 180, bird.action * 160, 180, 160, bird.x, bird.y)
        else:
            bird.image.clip_composite_draw(int(bird.frame%5) * 180, bird.action * 160, 180, 160, 0, 'h', bird.x, bird.y, 180, 160)



class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Fly
        self.transitions = {
                }

    def start(self):
        self.cur_state.enter(self.bird, ('Fly', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def draw(self):
        self.cur_state.draw(self.bird)





class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100, 1400), random.randint(100, 600)
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-60, self.y+50, f'{get_time()}', (255, 255, 0))
