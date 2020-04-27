#!/usr/bin/env python3

'''
Loads the song graph and gets going!
'''

import pickle
from listen.listener import *
from graph_logic.graph_playlist import generate_playlist
import listen_along_dj as ldj
import api_functions.misc_functions as sapi


def load_graph():
	with open('disk/song_map.pickle', 'rb') as fd:
		graph = pickle.load(fd)
	return graph

def autonomous_car_dj(listener, song_graph):
	'''
	Creates a walk along the song graph and queues up the songs
	'''

	playlist = generate_playlist(song_graph, 10)
	
	# Play the first song, queue the rest
	listener.play_track(playlist[0])
	
	for track in playlist[1:]:
		listener.queue_track(track)
	

	# Start a listen along DJ
	ldj.listen_along_dj(listener)

def initialise_listener():
	sp = sapi.create_sp()
	device_id = sapi.choose_device(sp)
	listen = listener(sp, device_id)
	return listen

def main():
	listener = initialise_listener()
	song_graph = load_graph()
	autonomous_car_dj(listener, song_graph)

if __name__ == '__main__':
	main()
