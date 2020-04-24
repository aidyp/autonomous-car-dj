import threading
from listen.listener import *
from api_functions.misc_functions import get_device_by_name



def check_song_change(listener, song_state):
	'''
	Checks if the player has moved on from the current song state
	song_state comes in as uri

	If there has been a song change, it will update the song graph
	'''
	# Start a timer
	threading.Timer(10.0, check_song_change).start()
	
	current_song = listener.get_current_song()
	if current_song != song_state:
		listener.update_graph
	
def listen_along_dj(listener):
	'''
	Control loop for the listen along DJ. 
	'''
	

	quit = 0
	song_state
	while quit < 1:
		
