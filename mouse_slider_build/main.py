# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:41:44 2021

@author: Paradeisios
"""
import os
from psychopy import visual, gui

from exp_code.tutorial import tutorial
from exp_code.experiment import experiment


def main():

    log_gui = gui.Dlg(title="Social Synchrony Pilot")

    log_gui.addField('Name:')
    log_gui.addField('Age:')
    log_data = log_gui.show()

    if log_gui.OK:  # or if ok_data is not None
        win = visual.Window(size=[1024, 1080],
                            units="pix",
                            fullscr=True,
                            color=(-1,-1,-1))

        parent_dir = os.getcwd()

        tutorial_movie = os.path.join(parent_dir, "videos", "test.mp4")
        image = os.path.join(parent_dir, "videos", "mouse_button.jpg")
        exp_video = os.path.join(parent_dir, "videos", "Forrest_Jenny_college.mp4")
        start_image=os.path.join(parent_dir, "videos", "start.png")
        pause_image=os.path.join(parent_dir, "videos", "pause.png")
        
        tutorial(win=win,
                  tutorial_movie=tutorial_movie,
                  image=image)

        experiment(win=win,
                   exp_video=exp_video,
                   log_data=log_data,
                   start_image=start_image,
                   pause_image=pause_image)

    else:
        print('user cancelled')


if __name__ == "__main__":
    main()
