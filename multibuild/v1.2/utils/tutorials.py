from psychopy import visual,event,core, monitors
from .constants import *
from .routines import *
import os
import time
from .experiments import *

def tutorial(exp, demographics_data, func, exp_name):
    if exp != 'general':
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
    else:
        WIDTH = 1920
        HEIGHT = 1080
    
        win = visual.Window(size=(WIDTH, HEIGHT),units="pix",color=(-1,-1,-1))
        work_folder = os.path.join(os.getcwd(),"assets","pics",exp)
        pictures = [os.path.join(work_folder,file) for file in os.listdir(work_folder)]
        myMouse = event.Mouse()
        
    # based on 'tutorial' function but used in cases where the exmples are videos
    # prepare all slides without videos, every slide there's a video should be blank.
    # in our case we have [Slide1,Slide2...Slide8] and we present videos named 'movie<n-1>' as follows:
    # 'summer1' on Slide2 (blank), 'summer3' on Slide4 (blank), summer5 on Slide6 (blank)
    
        for i,picture in enumerate(pictures):
            if i==1 or i==3 or i==5: # as explained above, video names will be named as summer(i).mp4
            
                movie = visual.MovieStim3(win=win, filename=os.path.join(os.getcwd(),"assets","exmp", "summer"+str(i)+".mkv"))
                #movie = visual.MovieStim3(win=win, filename=os.path.join(os.getcwd(),"assets","exmp", "summer"+str(i)+".mp4"))
                movie.size /= 1.2
                movie.size = np.round(movie.size)
                x = 0
                y = win.size[1]/2 - movie.size[1]/2
                movie.pos = (x,y)
                mouse = event.Mouse(win=win,visible=True)
    
                global stoped_before_time
                stoped_before_time = False
            
                movie.draw()
                movie.play()
            
                while movie.status != constants.FINISHED:
                    frame_time = movie.getCurrentFrameTime()
                    movie.draw()
                    win.flip()
           
     # tutorial skip using 'q' 
    
                    if len(event.getKeys(keyList=["q"]))>0:
                        stoped_before_time = True
                        break
            
                    if stoped_before_time:
                        time.sleep(1)
                        break
                    
                movie.stop()
        
            else: # insert instruction slide
                time.sleep(0.5)
                event.clearEvents()
                slide = visual.ImageStim(win=win,image=picture)
                while True:
                    slide.draw()
                    win.flip()
                    if len(event.getKeys(keyList=["right"])) > 0: #or myMouse.getPressed()[0] == 1:
                        event.clearEvents()
                        break
            win.flip()
            core.wait(1)
            
        win.close()       
        func(demographics_data, exp_name)