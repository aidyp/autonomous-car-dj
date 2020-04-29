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

def search_for_song(song, listener, song_graph):
	song_uri = listener.search_song(song)['uri']
	if song_uri in song_graph:
		return song_uri
	else:
		print("Can't find that one, picking for you!")
		return None

def pretty_print_queue(play_queue, listener):
	'''
	Pretty prints to the queue
	'''
	print("Now playing, ")
	for i in range(0, len(play_queue)):
		print(str(i + 1) + "] " + listener.pretty_name_by_uri(play_queue[i]))

def autonomous_car_dj(listener, song_graph):
	'''
	Creates a walk along the song graph and queues up the songs
	'''

	# First clear the queue (doesn't work)
	#listener.clear_spotify_queue()

	# Ask if the user has a song they want to start with
	inp = input("What song do you want to start with? (r for random): ")
	first_song = search_for_song(inp, listener, song_graph)

	playlist = generate_playlist(first_song, song_graph, 10)

	# Play the first song, queue the rest
	listener.play_track(playlist[0])

	for track in playlist[1:]:
		listener.queue_track(track)

	#pretty_print_queue(playlist, listener)
	inp = input("Want to drop into the listener? (y/n): ")
	if inp == 'y':
		# Start a listen along DJ if the user wants
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
