# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:51:26 2021

@author: Paradeisios
"""

from psychopy import visual,core,logging,constants,event
import numpy as np
import sys,os

def experiment(win,exp_video,log_data,start_image,pause_image):
    
    """ The main experiment. Works by 
    1. Creating a logger text that record timestap and rating for each frame (approximately)
    2. Projects the movie and the slider on the screen
    3. Keeps playing the movie and updating the slider 
    4. If subject hits q, movie will close  """
    

    log = ""
    log += f"Name, {log_data[0]}\n"
    log += f"Age,{log_data[1]}\n"
    log += "Timestap,Rating\n"
    
    text = visual.TextStim(win=win)
    text.text = "Loading experiment movie..."
    text.draw()
    win.flip()
    

    mov = visual.MovieStim3(win=win,filename=exp_video)
    mov.size /= 2
    mov.size = np.round(mov.size)
    x = 0
    y = win.size[1]/2 - mov.size[1]/2
    mov.pos = (x,y)
    
    
    # tqdm progress    
    video_tracker_bg = visual.Rect(win=win,
                                   lineColor="green",
                                   fillColor="black",
                                   pos=(0,-150),
                                   width=400,
                                   height=20)
    
    video_tracker_tqdm = visual.Rect(win=win,
                                   lineColor="green",
                                   fillColor="green",
                                   pos=(-200,-150),
                                   width=1,
                                   height=20)
    
    tqdm_text = visual.TextStim(win=win,
                                text=f"{mov.getCurrentFrameTime()}/{mov.duration}",
                                pos = (280,-150))
 
    ####### stop and play buttons
    start_button = visual.ImageStim(win=win,
                                    image=start_image,
                                    pos=(-350,-150),
                                    size=(50,50))
    stop_button  = visual.ImageStim(win=win,
                                    image=pause_image,
                                    pos=(-280,-150),
                                    size=(50,50))
    line = visual.Line(win=win,
                       lineColor=[1, 1, 1],
                       start=(-300,-250),
                       end=(300,-250),
                       lineWidth=5,
                       interpolate=True)
    
    circle = visual.Circle(win=win,
                       radius=20,
                       pos=(0,-250),
                       fillColor="red",
                       edges=128)
    
    mouse = event.Mouse(win=win,visible=True)
 
    text.text="Move the slider by moving the mouse\nPress space to begin\nPress q to exit the experiment"
    text.draw()
    win.flip()
    event.waitKeys(keyList=["space"])
    
    for i in range(3,0,-1):
        text.text = i
        text.draw()
        win.flip()
        core.wait(1)
        
    mouse.setPos(newPos=(0, -250))
    mouse.setVisible(1)
    
    paused = False
    
    while mov.status != constants.FINISHED:
        line.draw()
        circle.draw()
        mov.draw()
        
        video_tracker_bg.draw()
        curr_perc = mov.getCurrentFrameTime() * mov.duration / 100 
        x = -200 + curr_perc
        video_tracker_tqdm.pos=(x,-150)
        width = curr_perc*2
        video_tracker_tqdm.width=width
        video_tracker_tqdm.draw()
        tqdm_text.text = f"{np.round(mov.getCurrentFrameTime(),1)}/{mov.duration}"
        tqdm_text.draw()
        
        start_button.draw()
        stop_button.draw()
        
        win.flip()
        
        if mouse.isPressedIn(stop_button):
            mov.pause()
            paused = True
            
                
        if mouse.isPressedIn(start_button):
            mov.play()
            paused = False
 
    
           
        if (mouse.getPos()[0] < 300) and (mouse.getPos()[0] > -300) and not paused:
            circle.pos = (mouse.getPos()[0],-250)
            log +=f"{np.round(mov.getCurrentFrameTime(),3)},{circle.pos[0]}\n"
    
        
        if len(event.getKeys(keyList=["q"]))>0:
            log += f"{np.round(mov.getCurrentFrameTime(),3)},Experiment ended before movie end"
            break
        
    mov.stop()
    win.close()
    
    with open(f"{log_data[0]}_movie_output.txt","w") as logger:
        logger.write(log)
     
    sys.exit()

