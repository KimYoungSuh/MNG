from pico2d import *

class InputSys:
    move_state = 0
    last_vertical = 0
    last_horizon = 0
#
    def Get_move(self, event):
        if (event.type == SDL_KEYDOWN):
            if (event.key==SDLK_UP):
                InputSys.move_state = InputSys.move_state | 0b1000
                InputSys.last_vertical = 1
            elif (event.key==SDLK_DOWN):
                InputSys.move_state = InputSys.move_state | 0b0100
                InputSys.last_vertical = -1
            elif (event.key==SDLK_LEFT):
                InputSys.move_state = InputSys.move_state | 0b0010
                InputSys.last_horizon = -1
            elif (event.key==SDLK_RIGHT):
                InputSys.move_state = InputSys.move_state | 0b0001
                InputSys.last_horizon = 1
        if(event.type == SDL_KEYUP):
            if (event.key==SDLK_UP):
                InputSys.move_state = InputSys.move_state & 0b0111
                InputSys.last_vertical = -1
            elif (event.key==SDLK_DOWN):
                InputSys.move_state = InputSys.move_state & 0b1011
                InputSys.last_vertical = 1
            elif (event.key==SDLK_LEFT):
                InputSys.move_state = InputSys.move_state & 0b1101
                InputSys.last_horizon = 1
            elif (event.key==SDLK_RIGHT):
                InputSys.move_state = InputSys.move_state & 0b1110
                InputSys.last_horizon = -1
        return InputSys.move_state

    def Get_last_vertical(self):
        return InputSys.last_vertical
    def Get_last_horizon(self):
        return InputSys.last_horizon

    def Get_shoot_key(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            return  True
        else:
            return  False
