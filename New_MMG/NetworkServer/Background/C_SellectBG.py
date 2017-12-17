from pico2d import *

class C_SellectBG:
    def __init__(self):
        self.image = load_image('..\BackGround\Image_SelectBG.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
