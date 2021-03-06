from pico2d import *
from Bullet.C_EnemyBullet import EBullet

_Bullet = []

class Enemy2:
    image = None

    def __init__(self, X, Y,State, BG_X, BG_Y):
        self.x, self.y = X, Y
        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y
        self.state = State

        if Enemy2.image == None:
            Enemy2.image = load_image('Resource\Image_Enermy2.png')

    def returnDir(self, x,y):
        pass

    def update(self, X, Y, State,BG_X, BG_Y):
        self.sx = X - BG_X
        self.sy = Y - BG_Y
        self.state = State

    def add(self,PL_X, PL_Y):
        if self.Whattime >= 2.0:
            EBullet(self.x, self.y, PL_X,PL_Y)
            self.Whattime = 0

    def draw(self):
        Scean_x, Scean_y = 49, 82
        self.image.clip_draw(0, 0, Scean_x, Scean_y, self.sx, self.sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx-10 , self.sy-10, self.sx+10, self.sy+10

def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)




