from utils.routines import *
import psychopy as ps

requirements()
consent("consent1.JPG", False)
consent("consent2.JPG", False)
consent("consent3.JPG", True)

log_data = demographics()  # get demographics

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

# for testing - write 'test' under 'Age' in the demographics gui 
if log_data[0][0] == 'test': 
    specify_experiment_phase(log_data)
else:
    specify_experiment_phase_random(log_data)

consent("debrief.jpg", False)