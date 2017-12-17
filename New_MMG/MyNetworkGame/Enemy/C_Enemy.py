from pico2d import *

_Bullet = []

class Enemy1:
    image =None
    def __init__(self, X, Y, State, BG_X, BG_Y):
        global font
        self.x, self.y = X , Y
        self.sx = self.x - BG_X
        self.sy = self.y - BG_Y
        self.state =State
        if Enemy1.image == None:
            Enemy1.image = load_image('Resource\Image_Enermy.png')

    def returnx(self):
        return self.x

    def returny(self) :
        return self.y

    def update(self, X, Y, State,BG_X, BG_Y):
        self.sx = X - BG_X
        self.sy = Y - BG_Y

    def draw(self):
        self.image.draw(self.sx, self.sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.sx-10 , self.sy-10, self.sx+10, self.sy+10

def delete_object(objects):
    for object in objects:
        if object.alive == 0:
            objects.remove(object)




