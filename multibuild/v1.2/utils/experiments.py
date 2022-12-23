
from psychopy import visual, core, logging, constants, event, monitors
import numpy as np
import sys,os
import pdb

from wx.core import Width
from .constants import *
import random, string
import math
import utils.routines
import threading
import time


tages_results = []
paused = False
log = ""
stoped_before_time = False

def async_logger_sync(movie, circle, mouse):
    global tages_results
    global paused
    global log
    global stoped_before_time

    while movie.status != constants.FINISHED:
        time.sleep(0.1) # sample at 0.1 Hz
        
        if (mouse.getPos()[0] < 300) and (mouse.getPos()[0] > -300) and not paused and not stoped_before_time:
            circle.pos = (mouse.getPos()[0],-450)
        elif not paused and not stoped_before_time:
            if mouse.getPos()[0] < 0:
                circle.pos = (-300,-450)
            else:
                circle.pos = (300,-450)
        else:
        	continue
        if stoped_before_time:
        	break
        else:
            try:
                frame_time = movie.getCurrentFrameTime()
            except:
                frame_time = None

        if frame_time != None:
            log +=f"{np.round(frame_time,1)},{circle.pos[0]}\n"
            tages_results.append([np.round(frame_time,1),circle.pos[0]])
            #print([np.round(frame_time,1),circle.pos[0]])

def async_logger_arousal(movie, pointer, mouse):
    global tages_results
    global paused
    global log
    global stoped_before_time

    while movie.status != constants.FINISHED:
        time.sleep(0.1)

        pointer.pos = mouse.getPos()
        
        dist = math.sqrt((pointer.pos[0] - (-400)) ** 2 + (pointer.pos[1] - (0)) ** 2)

        if dist > 310:
            xm = pointer.pos[0]
            ym = pointer.pos[1]            

            ym_square = ym**2
            xm_helper = (xm+400) ** 2

            a = (ym_square/xm_helper) + 1
            b = ((800*ym_square) / xm_helper) + 800
            c = (((400*ym)**2) / xm_helper) + (400**2 - 310**2)

            asqrt = math.sqrt((b**2) - (4*a*c))
            x1 = ((-1*b) + asqrt) / (2*a)
            x2 = ((-1*b) - asqrt) / (2*a)

            first_option = (x1, ((ym/(xm+400))*x1) + ((400*ym)/(xm+400)) )
            second_option = (x2, ((ym/(xm+400))*x2) + ((400*ym)/(xm+400)) )

            dist1 = math.sqrt((xm - first_option[0]) ** 2 + (ym - first_option[1]) ** 2)
            dist2 = math.sqrt((xm - second_option[0]) ** 2 + (ym - second_option[1]) ** 2)

            if dist1 < dist2:
                pointer.pos[0] = first_option[0]
                pointer.pos[1] = first_option[1]
            else:
                pointer.pos[0] = second_option[0]
                pointer.pos[1] = second_option[1]

        if stoped_before_time:
        	break
        else:
            try:
                frame_time = movie.getCurrentFrameTime()
            except:
                frame_time = None
        if paused:
        	continue

        if frame_time != None:
            log += f"{np.round(frame_time,1)}, {pointer.pos[0]}, {pointer.pos[1]}\n"
            tages_results.append([frame_time, pointer.pos[0], pointer.pos[1]])
            #print([np.round(frame_time,1), pointer.pos[0], pointer.pos[1]])

def sync_experiment(user_data, exp_name):
    movie_fname = utils.routines.get_random_movie_if_not_picked()  #select movie
    if movie_fname == None:
        print('problem with movie selection!')
        return 

    demographics_data = user_data[0]
    timeStamp = user_data[0][-1]
    global log

    log = ""
    #log += f"Name,{demographics_data[0]}\n"
    log += f"Version,1.2\n"
    log += f"Age,{demographics_data[0]}\n"
    log += f"Gender,{demographics_data[1]}\n"
    log += f"Seen,{demographics_data[2]}\n"
    log += f"Birth,{demographics_data[3]}\n"
    log += f"Education,{demographics_data[4]}\n"
    log += f"LivesWith,{demographics_data[5]}\n"
    log += f"Movie,{os.path.basename(movie_fname)}\n"
    log += f"Experiment,{exp_name}\n"
    log += f"Tutorial1,{user_data[2]}\n"
    log += f"Tutorial2,{user_data[3]}\n"
    log += f"Consent,{timeStamp}\n"
    log += "Time,X\n"

    WIDTH = 1920
    HEIGHT = 1080

    win = visual.Window(size=(WIDTH,HEIGHT),units="pix",color=(-1,-1,-1))
    text = visual.TextStim(win=win,text="Loading experiment movie...")
    text.draw()
    win.flip()
    
    line = visual.Line(win=win,
                       lineColor=[1, 1, 1],
                       start=(-300,-450),
                       end=(300,-450),
                       lineWidth=5,
                       interpolate=True)

    left_bar_text = visual.TextStim(win=win, text="No sync", pos=(-400, -450))
    right_bar_text = visual.TextStim(win=win, text="Max sync", pos=(400, -450))

    circle = visual.Circle(win=win,
                           radius=20,
                           pos=(0,-450),
                           fillColor="red",
                           edges=128)
    
    mouse = event.Mouse(win=win,visible=False) 
    
    movie = visual.MovieStim3(win=win,filename=movie_fname,loop=False)
    movie.size /= 1.2
    movie.size = np.round(movie.size)
    x = 0
    y = win.size[1]/2 - movie.size[1]/1.8
    movie.pos = (x,y)
    
    text.text="Move the slider by moving the mouse\nPress space to begin\nPress q to exit the experiment\n Press p to pause and c to continue"
    text.draw()
    win.flip()
    event.waitKeys(keyList=["space"])
    
    for i in range(3,0,-1):
        text.text = i
        text.draw()
        win.flip()
        core.wait(1)
        
    mouse.setPos(newPos=(0, -250))
    mouse.setVisible(0) # hide mouse 
    
    paused = False
    stoped_before_time = False

    t = threading.Thread(target = async_logger_sync, args=(movie, circle, mouse))
    t.start()
    win.flip()
    #movie.play()
    
    while movie.status != constants.FINISHED:
        if not paused:
            line.draw()
            left_bar_text.draw()
            right_bar_text.draw()
            circle.draw()
            movie.draw()
            win.flip()

        # pause using 'p' on keyboard
        if len(event.getKeys(keyList=["p"]))>0:
            paused = True 
            movie.pause()
            event.clearEvents()
            
        # play using 'c' on keyboard    
        if len(event.getKeys(keyList=["c"]))>0:
            paused = False
            movie.play()
            event.clearEvents()

        if len(event.getKeys(keyList=["q"]))>0:
            stoped_before_time = True
            event.clearEvents()
            break

    if stoped_before_time:
        log += f"{np.round(movie.getCurrentFrameTime(), 3)},Experiment ended before movie end"
        time.sleep(1)
        
    movie.stop()
    win.close()
    time.sleep(1) # added 20.12.22 by Ariel
    
    random_ascii = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    fname = os.path.join(os.getcwd(),"output",random_ascii + ("_movie_output_%d.csv" % (user_data[1],)) )
    dir_to_create = os.path.join(os.getcwd(),"output")
    try:
        os.makedirs(dir_to_create)
    except:
        pass
    print(fname)

    with open(fname,"w") as logger:
        logger.write(log)
    user_data[1]+=1
    
    
# the entire function is depricated as we do not use arousel experiment
def arousal_experiment(user_data, exp_name):
    movie_fname = utils.routines.get_random_movie_if_not_picked()  #select movie
    if movie_fname == None:
        return

    demographics_data = user_data[0]
    global log

    log = ""
    log += f"Name,{demographics_data[0]}\n"
    log += f"Age,{demographics_data[0]}\n"
    log += f"Gender,{demographics_data[1]}\n"
    log += f"Seen,{demographics_data[2]}\n"
    log += f"Birth,{demographics_data[3]}\n"
    log += f"Exp_with_coding,{demographics_data[4]}\n"
    log += f"Education,{demographics_data[5]}\n"
    log += f"Movie,{os.path.basename(movie_fname)}\n"
    log += f"Experiment,{exp_name}\n"
    log += f"Tutorial1,{user_data[2]}\n"
    log += f"Tutorial2,{user_data[3]}\n"
    log += "Time,X,Y\n"

    WIDTH = 1920
    HEIGHT = 1080

    win = visual.Window(size=(WIDTH,HEIGHT),units="pix",color=(-1,-1,-1))

    text = visual.TextStim(win=win,text="Loading experiment movie...")
    text.draw()
    win.flip()

    arousal_grid = os.path.join(os.getcwd(), "assets","pics", AROUSAL)
    pic = visual.ImageStim(win=win,image= arousal_grid,size=(700,700),pos=(-400,0))
    mov = visual.MovieStim3(win=win,filename=movie_fname,size=(800,600),pos=(450,0))
    pointer = visual.Circle(win=win,pos=(0,0),units="pix",radius=10,fillColor=[1, -1, -1],edges=128,opacity=.8)

    mouse = event.Mouse(win=win,visible=True) # changed to True

    start_image = os.path.join(os.getcwd(), "assets","pics", BUTTONS[0])
    stop_image =  os.path.join(os.getcwd(), "assets","pics", BUTTONS[1])
    start_button = visual.ImageStim(win=win,image=start_image,pos=(330,-400),size=(70,70))
    stop_button  = visual.ImageStim(win=win,image=stop_image,pos=(480,-400),size=(70,70))

    text.text="Move the slider by moving the mouse\nPress space to begin\nPress q to exit the experiment"
    text.draw()
    win.flip()
    event.waitKeys(keyList=["space"])
    
    for i in range(3,0,-1):
        text.text = i
        text.draw()
        win.flip()
        core.wait(1)
        
    mouse.setPos(newPos=(-180, 0))
    mouse.setVisible(0) 

    global tages_results
    global paused
    global stoped_before_time

    tages_results = []
    stoped_before_time = False
    paused = False

    t = threading.Thread(target = async_logger_arousal, args=(mov, pointer, mouse))
    t.start()

    while mov.status != constants.FINISHED: 
        start_button.draw()
        stop_button.draw()
        if not paused:
            pic.draw()
            mov.draw()
            pointer.draw()
            win.flip()
        
        if len(event.getKeys(keyList=["q"]))>0:
            break

        if mouse.isPressedIn(stop_button):
            paused = True    
                
        if mouse.isPressedIn(start_button): 
            paused = False
            event.clearEvents()
 
        if paused:
            mov.pause()
        else:
            mov.play()

        if len(event.getKeys(keyList=["q"]))>0:
            stoped_before_time = True
            break

    if stoped_before_time:
        time.sleep(1)
        log += f"{np.round(mov.getCurrentFrameTime(), 3)},Experiment ended before movie end"
        
    mov.stop()
    win.close()

    random_ascii = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    fname = os.path.join(os.getcwd(),"output",random_ascii + ("_movie_output_%d.csv" % (user_data[1],)) )
    dir_to_create = os.path.join(os.getcwd(),"output")
    try:    
        os.makedirs(dir_to_create)
    except:
        pass
    print(fname)

    with open(fname,"w") as logger:
        logger.write(log)
    user_data[1]+=1