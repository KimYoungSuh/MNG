from pico2d import *

'''
moveState는 비트 연산자로 0b0000 각각 상하좌우순
'''

class InputSys:

    def __init__(self):
        self.moveState = 0

    def Move(self, events):
        for event in events:
            if (event.type == SDL_KEYDOWN):
                if (event.key==SDLK_UP):
                    self.moveState = self.moveState | 0b1000
                elif (event.key==SDLK_DOWN):
                    self.moveState = self.moveState | 0b0100
                elif (event.key==SDLK_LEFT):
                    self.moveState = self.moveState | 0b0010
                elif (event.key==SDLK_RIGHT):
                    self.moveState = self.moveState | 0b0001
            if(event.type == SDL_KEYUP):
                if (event.key==SDLK_UP):
                    self.moveState = self.moveState & 0b0111
                elif (event.key==SDLK_DOWN):
                    self.moveState = self.moveState & 0b1011
                elif (event.key==SDLK_LEFT):
                    self.moveState = self.moveState & 0b1101
                elif (event.key==SDLK_RIGHT):
                    self.moveState = self.moveState & 0b1110

    def Test(self):
        print(bin(self.moveState))
