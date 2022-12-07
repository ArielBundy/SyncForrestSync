from psychopy import visual,core,event,constants,logging
import numpy as np

output_file = "movie_output.log"
log = logging.LogFile(f=output_file)

win = visual.Window(size=[1280,1024],
                    units="pix",
                    fullscr=False,
                    color=[-1, -1, -1])

mov = visual.MovieStim3(win=win,
                        filename="test.mp4")
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



clock = core.Clock()
log.write("Timestap,Rating\n")

def move_left(win,mov,line,circle,log):
    

    circle.pos -= (100,0)
    line.draw()
    circle.draw()
    mov.draw()
    log.write(f"{np.round(clock.getTime(),3)},{circle.pos[0]}\n")


def move_right(win,mov,line,circle,log):
    circle.pos += (100,0)
    line.draw()
    circle.draw()
    mov.draw()
    log.write(f"{np.round(clock.getTime(),3)},{circle.pos[0]}\n")

event.globalKeys.clear()
event.globalKeys.add(key="left",
                     func=move_left,
                     func_args=(win,mov,line,circle,log))
event.globalKeys.add(key="right",
                     func=move_right,
                     func_args=(win,mov,line,circle,log))

text = visual.TextStim(win=win, 
                       text="Move the slider by pressing left or right\nPress space to begin")
text.draw()
win.flip()
event.waitKeys(keyList=["space"])

for i in range(3,0,-1):
    text.text = i
    text.draw()
    win.flip()
    core.wait(1)

clock.reset()
while mov.status != constants.FINISHED:
    line.draw()
    circle.draw()
    mov.draw()
    win.flip()
    log.write(f"{np.round(clock.getTime(),3)},{circle.pos[0]}\n")
mov.stop()
win.close()

