# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:33:20 2021

@author: Paradeisios
"""
from psychopy import visual,event,constants,core
import numpy as np


def tutorial(win,tutorial_movie,image):
    
    mov = visual.MovieStim3(win=win,
                            filename=tutorial_movie)
    
    mov.size /= 2
    mov.size = np.round(mov.size)
    x = 0
    y = win.size[1]/2 - mov.size[1]/2
    mov.pos = (x,y)
    
    line = visual.Line(win=win,
                   lineColor=[1, 1, 1],
                   start=(-300,-200),
                   end=(300,-200),
                   lineWidth=5,
                   interpolate=True)

    circle = visual.Circle(win=win,
                   radius=20,
                   pos=(0,-200),
                   fillColor="red",
                   edges=128)
    
    text = visual.TextStim(win=win)
    
    mouse = event.Mouse(win=win,visible=False)

    mouse_button = visual.ImageStim(win=win,
                                image=image,
                                pos=(0,-200),
                                size = (20,20))
    
    text.text = "In this experiment, you will .......\nPlease use the slider below to rate the synchrony as it will be shown now\nPress space to start the tutorial"
    text.draw()
    win.flip()
    
    event.waitKeys(keyList=["space"])
     
    high_sync = False
    low_sync  = False
    while mov.status != constants.FINISHED:
        
        mov.draw()
        line.draw()
        circle.draw()
        mouse_button.draw()
        win.flip()
        
        if (np.round(mov.getCurrentFrameTime(),2) == 6.08) and not high_sync :
            
            mov.pause()
            text.text = "This is a scene of high synchrony, so the slider will be dragged to the right"
            text.pos = (0,-250)
            win.flip()
            
            for i in range(30):
                circle.pos += (7,0)
                mouse_button.pos += (7,0)
                line.draw()
                circle.draw()
                mouse_button.draw()
                mov.draw()
                text.draw()
                win.flip()
                core.wait(.05)
            
            high_sync = True
            core.wait(2)
            mov.play()
             
        
        if (np.round(mov.getCurrentFrameTime(),2) == 8.08) and not low_sync:
            
            mov.pause()
            text.text = "This is a scene of low synchrony, so the slider will be dragged to the left"
            text.pos = (0,-250)
            win.flip()
            
            for i in range(30):
                circle.pos -= (7,0)
                mouse_button.pos -= (7,0)
                line.draw()
                circle.draw()
                mouse_button.draw()
                mov.draw()
                text.draw()
                win.flip()
                core.wait(.05)
            
            low_sync = True
            core.wait(2)
            mov.play()
            
    text.text = "End of Tutorial"
    text.draw()  
    win.flip()
    core.wait(2)
        
         