#!/usr/bin/env python3

'''
Loads the song graph and gets going!
'''

import pickle
from listen.listener import *
from graph_logic.graph_playlist import generate_playlist
from api_functions.misc_functions import get_device_by_name
import listen_along_dj as ldj


def load_graph():
	with open('disk/song_map.pickle', 'rb') as fd:
		graph = pickle.load(fd)
	return graph

def autonomous_car_dj(listener, song_graph):
	'''
	Creates a walk along the song graph and queues up the songs
	'''

	playlist = generate_playlist(song_graph, 6)
	
	# Play the first song, queue the rest
	listener.play_track(playlist[0])
	
	for track in playlist[1:]:
		listener.queue_track(track)
	

	# Start a listen along DJ
	ldj.main()

def initialise_listener():
	scope = 'user-read-playback-state,user-modify-playback-state'
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))
	device_id = get_device_by_name('kanga', sp)
	listen = listener(sp, device_id)
	return listen

def main():
	listener = initialise_listener()
	song_graph = load_graph()
	autonomous_car_dj(listener, song_graph)

if __name__ == '__main__':
	main()
