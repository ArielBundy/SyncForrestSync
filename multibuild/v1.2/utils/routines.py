from tkinter import *
from tkinter import filedialog
from psychopy import gui, monitors
from .tutorials import *
from .experiments import *
import os
import sys
import time
import random

picked_movies = []


def consent(filename, should_checkbox):

    win = visual.Window(size=(1280,720), units="pix", color=(-1,-1,-1))
    mouse = event.Mouse(win=win,visible=True)

    last_press_check = 0
    last_press_continue = 0
    press_error = 0.2
    is_pressed = False

    consent_image = os.path.join(os.getcwd(),"assets","consent","consent", filename)
    checkbox_unmarked_image = os.path.join(os.getcwd(),"assets","pics","checkbox_unmarked.png")
    checkbox_marked_image = os.path.join(os.getcwd(),"assets","pics","checkbox_marked.png")
    continue_image = os.path.join(os.getcwd(),"assets","pics","continue.png")

    consent = visual.ImageStim(win=win, size=(WIDTH, HEIGHT), units="pix", image=consent_image)
    checkbox = visual.ImageStim(win=win, image=checkbox_unmarked_image, size=(70,70), pos=(600, -300))
    continue_btn = visual.ImageStim(win=win, image=continue_image,pos=(450, -300))

    while True:
        consent.draw()
        if should_checkbox:
            checkbox.draw()
        continue_btn.draw()
        win.flip()
        
        if should_checkbox:
            if mouse.isPressedIn(checkbox) and not is_pressed and (time.time() - last_press_check) > press_error:
                last_press_check = time.time()
                is_pressed = True
                checkbox.setImage(checkbox_marked_image)

            if mouse.isPressedIn(checkbox) and is_pressed and (time.time() - last_press_check) > press_error:
                last_press_check = time.time()
                is_pressed = False
                checkbox.setImage(checkbox_unmarked_image)

            if mouse.isPressedIn(continue_btn) and (time.time() - last_press_continue) > press_error:
                last_press_continue = time.time()
                if is_pressed:
                    break
        else:
            if mouse.isPressedIn(continue_btn):
                break
        #if len(event.getKeys(keyList=["right"])):
        #    break
        event.clearEvents()
    win.close()

firstMovieSuccess = 0
secondMovieSuccess = 0

def countOnes(num):
    count = 0

    while num > 0:
        count += num & 1
        num = num >> 1
    return count

def checkFuncFirst(time, circle): 
    global firstMovieSuccess

    cur_time = time
    cur_pos = int(circle.pos[0])

    criterias = [ \
    (cur_time >= 0 and cur_time <= 4 and cur_pos <= -150), \
    (cur_time >= 5 and cur_time <= 12 and cur_pos >= 150), \
    (cur_time >= 19 and cur_time <= 20 and cur_pos >= 150), \
    (cur_time >= 24 and cur_time <= 28 and cur_pos <= -150), \
    (cur_time >= 29 and cur_time <= 30 and cur_pos >= 150), \
    (cur_time >= 30 and cur_pos >= 150)
    ]

    for i in range(0, len(criterias)):
        if criterias[i]:
            firstMovieSuccess = firstMovieSuccess | (2 ** i)

def checkFuncSecond(time, circle): 
    global secondMovieSuccess

    cur_time = time
    cur_pos = int(circle.pos[0])

    criterias = [ \
    (cur_time >= 17 and cur_time <= 21 and cur_pos >= 150)
    ]

    for i in range(0, len(criterias)):
        if criterias[i]:
            secondMovieSuccess = secondMovieSuccess | (2 ** i)

def displayMovie(filename, isFirst, checkFunc):
    WIDTH = 1920
    HEIGHT = 1080

    global firstMovieSuccess
    global secondMovieSuccess

    isSuccess = True

    win = visual.Window(size=(WIDTH,HEIGHT),units="pix",color=(-1,-1,-1))
    
    movie = visual.MovieStim3(win=win, filename=os.path.join(os.getcwd(),"assets","slider_tutorial", filename))
    movie.size /= 1.5
    movie.size = np.round(movie.size)
    x = 0

    y = win.size[1]/2 - movie.size[1]/2
    movie.pos = (x,y)

    line = visual.Line(win=win,
                       lineColor=[1, 1, 1],
                       start=(-300,-450),
                       end=(300,-450),
                       lineWidth=5,
                       interpolate=True)

    if isFirst:
        left_bar_text = visual.TextStim(win=win, text="השבכ", pos=(-400, -450))
        right_bar_text = visual.TextStim(win=win, text="באז", pos=(400, -450))
    else:
        right_bar_text = visual.TextStim(win=win, text="רוביד", pos=(400, -450))

    circle = visual.Circle(win=win,
                           radius=20,
                           pos=(0,-450),
                           fillColor="red",
                           edges=128)

    mouse = event.Mouse(win=win,visible=True)

    #####################################################################
    # inserted 7.12.22 - stoped_before_time for tutorial skips 
    
    global stoped_before_time
    stoped_before_time = False
    
    #####################################################################
    while movie.status != constants.FINISHED:
        frame_time = movie.getCurrentFrameTime()

        line.draw()
        if isFirst:
            left_bar_text.draw()
        right_bar_text.draw()
        circle.draw()
        movie.draw()
        win.flip()
        movie.play()

        if (mouse.getPos()[0] < 300) and (mouse.getPos()[0] > -300):
            circle.pos = (mouse.getPos()[0],-450)
        else:
            if mouse.getPos()[0] < 0:
                circle.pos = (-300,-450)
            else:
                circle.pos = (300,-450)

        checkFunc(int(frame_time), circle)
        
    ##################################################################################################    
    # inserted 7.12.22 - tutorial skip using 'q' 
        if len(event.getKeys(keyList=["q"]))>0:
            stoped_before_time = True
            secondMovieSuccess = secondMovieSuccess | (2 ** 3)
            break
            
    if stoped_before_time:
        time.sleep(1)
    ##################################################################################################
    
    movie.stop()
    win.close()

    return countOnes(firstMovieSuccess) >= 4 if isFirst else countOnes(secondMovieSuccess) >= 1

def displaySlide(slide):
    WIDTH = 1920
    HEIGHT = 1080

    win = visual.Window(size=(WIDTH,HEIGHT),units="pix",color=(-1,-1,-1))
    mouse = event.Mouse(win=win,visible=True)

    slide_path = os.path.join(os.getcwd(),"assets","slider_tutorial", slide)

    slide = visual.ImageStim(win=win, image=slide_path)

    while True:
        slide.draw()
        win.flip()

        if len(event.getKeys(keyList=["right"])) > 0:# or mouse.getPressed()[0] == 1:
            event.clearEvents()
            break
        event.clearEvents()
    win.close()


def requirements():
    win = visual.Window(size=(WIDTH, HEIGHT), units="pix", color=(-1, -1, -1))
    mouse = event.Mouse(win=win , visible=True)

    consent_image = os.path.join(os.getcwd(),"assets","consent","consent", "requirements.jpg" )
    continue_image = os.path.join(os.getcwd(),"assets","pics","continue.png")

    consent = visual.ImageStim(win=win, image=consent_image)
    continue_btn = visual.ImageStim(win=win, image=continue_image,pos=(450, -300))

    while True:
        consent.draw()
        continue_btn.draw()
        win.flip()

        if mouse.isPressedIn(continue_btn):
            break
        event.clearEvents()
    win.close()

def restart_program():
    os.popen("python " + sys.argv[0])
    time.sleep(1)
    sys.exit()

def get_random_movie_if_not_picked():
    global picked_movies
    
    work_folder = os.path.join(os.getcwd(),"assets","movies")
    movies = [os.path.join(work_folder,file) for file in os.listdir(work_folder)]
    movies = [x for x in filter(lambda x : os.path.isfile(x) , movies)]

    movie = random.choice(movies)
    while movie in picked_movies:
        movies.remove(movie)
        if len(movies) == 0:
            break
        movie = random.choice(movies)

    if len(movies) == 0:
        return None

    picked_movies.append(movie)
    return movie

def select_movie():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

    
def specify_experiment_phase(demographics_data):
    
    # changes made 7.12.22 - disabled 'valance\arousel' in Testing mode.
    # uncomment arousal_button and it's grid if needed
    root = Tk()
    root.title("Social Synchrony Exp v1.2")

    gaze_button = Button(root,text="Gaze Synchrony",width=50,height=2,command=lambda: tutorial("gaze", demographics_data, sync_experiment, "Gaze Synchrony"))
    touch_button = Button(root, text="Touch Synchrony",width=50,height=2,command=lambda: tutorial("touch", demographics_data, sync_experiment, "Touch Synchrony"))
    affect_button = Button(root, text="Affect Synchrony",width=50,height=2,command=lambda: tutorial("affect", demographics_data, sync_experiment, "Affect Synchrony"))
    id_button =  Button(root,text="Identification",width=50,height=2,command=lambda: tutorial("id", demographics_data, sync_experiment, "Identification"))
    general_button = Button(root,text="General Synchrony",width=50,height=2,command=lambda: tutorialG("general", demographics_data, sync_experiment, "General Synchrony"))
    #arousal_button = Button(root, text="Valence/Arousal",width=50,height=2,command=lambda: tutorial("valance", demographics_data, arousal_experiment, "Valence/Arousal"))
    start_over_button = Button(root,text="Start over",width=50,height=2,command=lambda: restart_program())

    gaze_button.grid(row=1,column=0)
    touch_button.grid(row=2,column=0)
    affect_button.grid(row=3,column=0)
    general_button.grid(row=4,column=0)
    id_button.grid(row=5,column=0)
    #arousal_button.grid(row=6,column=0)
    start_over_button.grid(row=0,column=0)

    root.mainloop()

def specify_experiment_phase_random(demographics_data):
    calls = [
    ("gaze", demographics_data, sync_experiment, "Gaze Synchrony"), \
    ("touch", demographics_data, sync_experiment, "Touch Synchrony"), \
    ("affect", demographics_data, sync_experiment, "Affect Synchrony"), \
   # ("valence", demographics_data, arousal_experiment, "Valence/Arousal"), \
   # ("id", demographics_data, sync_experiment, "Identification"), \
    ("general", demographics_data, sync_experiment, "General Synchrony")
    ]
    
    first_choice = random.choice(calls)
    calls.remove(first_choice)
    second_choice = random.choice(calls)
    calls.remove(second_choice)
    tutorial(*first_choice)
    event.clearEvents()
    time.sleep(2)
    tutorial(*second_choice)

def demographics():

    log_gui = gui.Dlg(title="פרטים אישיים")
    log_gui.addField("Age:")
    log_gui.addField("Gender:", choices=["M","F","Other"])
    log_gui.addField("Have you seen the movie 'Forrest Gump' before:", choices=["Y","N"])
    log_gui.addField("Date of birth (dd/mm/yyyy):")
    #log_gui.addField("Do you have any experience with behavioral coding:", choices=["Y","N"])
    log_gui.addField("Educational Level:",choices=["Highschool","BA/BSc","MA/MSc","PhD","Engineering Degree"])
    log_gui.addField("You currenly live with",choices=["Parents/Siblings","Dorms/shared flat","With spouse","Alone"])

    log_data = log_gui.show()  
    if log_gui.OK: 
        print(log_data)
    else:
        print('user cancelled')
    return [log_data, 1]

