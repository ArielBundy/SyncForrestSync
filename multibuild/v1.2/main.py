from utils.routines import *
import psychopy as ps

requirements()
consent("consent1.JPG", False)
consent("consent2.JPG", False)
consent("consent3.JPG", True)

log_data = demographics()  #get demographics

SOUND_TEST_MODE = True

is_success_first = False
is_success_second = False

if True:
	displaySlide("slider_tutorial_1.jpg")
	is_success_first = displayMovie("mighty1.mp4", True, checkFuncFirst)

	if SOUND_TEST_MODE:
		while not is_success_second:
			displaySlide("slider_tutorial_2.jpg")
			is_success_second = displayMovie("mighty_2.mp4", False, checkFuncSecond)
			if not is_success_second:
				displaySlide("slider_tutorial_4.jpg")
	else:
		displaySlide("slider_tutorial_2.jpg")
		is_success_second = displayMovie("mighty_2.mp4", False, checkFuncSecond)

	displaySlide("slider_tutorial_3.jpg")

log_data.append(1 if is_success_first else 0)
log_data.append(1 if is_success_second else 0)
###########################################################################################################
# this box controls between Testing the experiment and actually running it
# Testing = 'specify_experiment_phase'
# Running = 'specify_experiment_phase_random'

# uncomment the one you need and comment the next below, default is Running:

specify_experiment_phase_random(log_data)
#specify_experiment_phase(log_data)
##########################################################################################################

consent("debrief.jpg", False)