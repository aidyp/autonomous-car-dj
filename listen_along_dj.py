import threading
from listen.listener import *
from api_functions.misc_functions import get_device_by_name
import sys



def check_song_change(args):
	'''
	Checks if the player has moved on from the current song state
	song_state comes in as uri

	If there has been a song change, it will update the song graph
	'''

	# Unpack the arguments
	listener = args[0]
	song_state = args[1]

	
	
	# Update the song graph for this listener
	current_song = listener.get_current_song_uri()
	if current_song != song_state:
		listener.update_graph(song_state)
		args[1] = current_song

	
	# Start a timer for the next check
	t = threading.Timer(15.0, check_song_change, args=(args,))
	t.daemon=True #song change thread should be subservient to main thread
	t.start()
	return
	
def listen_along_dj(listener):
	'''
	Control loop for the listen along DJ. 
	'''
	quit = 0
	song_state = listener.get_current_song_uri()
	# Start a timer
	check_song_change([listener, song_state])
	while quit < 1:
		inp = input("Search for a song to add it to your queue: ")
		
		if inp == 'quit':
			listener.write_graph()
			sys.exit()
		else:
			listener.process_and_add(inp)

def initialise():
	scope = 'user-read-playback-state,user-modify-playback-state'
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))
	device_id = get_device_by_name('kanga', sp)
	listen = listener(sp, device_id)
	return listen

if __name__ == '__main__':
	listen = initialise()
	listen_along_dj(listen)
