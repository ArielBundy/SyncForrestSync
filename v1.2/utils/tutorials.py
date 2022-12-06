from psychopy import visual,event,core, monitors
from .constants import *
from .routines import *
import os
import time
from .experiments import *

def tutorial(exp, demographics_data, func, exp_name):
    WIDTH = 1920
    HEIGHT = 1080
    win = visual.Window(size=(WIDTH, HEIGHT),units="pix",color=(-1,-1,-1))
    work_folder = os.path.join(os.getcwd(),"assets","pics",exp)
    pictures = [os.path.join(work_folder,file) for file in os.listdir(work_folder)]
    myMouse = event.Mouse()

    for picture in pictures:
        event.clearEvents()
        slide = visual.ImageStim(win=win,image=picture)
        while True:
            slide.draw()
            win.flip()
            if len(event.getKeys(keyList=["right"])) > 0: #or myMouse.getPressed()[0] == 1:
                event.clearEvents()
                break
            event.clearEvents()
    func(demographics_data, exp_name)
    win.close()
    
 
    


