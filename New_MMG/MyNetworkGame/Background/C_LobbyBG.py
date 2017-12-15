from pico2d import *

class C_LobbyBG:
    def __init__(self):
        self.image = load_image('..\Resource\Image_LobbyBG.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

    def draw(self):
        self.image.draw( self.canvas_width/2, self.canvas_height/2)

