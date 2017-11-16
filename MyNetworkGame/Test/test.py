from State.C_Input import InputSys
from pico2d import *

test =  InputSys()
open_canvas()
while(1):
    events=get_events()
    test.Move(events)
    test.Test()




