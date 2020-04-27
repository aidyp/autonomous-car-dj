#!/usr/bin/env python3

import threading
from listen.listener import *
import api_functions.misc_functions as sapi
import sys



def save_song_graph(args):
	'''
	The listener DJ usually only saves the song_graph on quit. This is just to make sure it does it a little more often
	'''
	listener = args[0]
	listener.write_graph()
	t = threading.Timer(60.0, save_song_graph, args=(args,))
	t.daemon=True
	t.start()

def check_song_change(args):
	'''
	Periodically checks if the song has changed. If it has, runs the update code
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


def command_switchboard(command, listener, song_state):
	'''
	Run if a command is entered prepended by '_'
	'''
	if command == 'quit':
		listener.update_graph(song_state)
		listener.write_graph()
		sys.exit()
	elif command == 'skip':
		listener.skip_song()
		listener.update_graph(song_state)
	elif command == 'undo':
		listener.pop_queue()
	else:
		print("Command not recognised, sorry!")

def listen_along_dj(listener):
	'''
	Control loop for the listen along DJ. 
	'''
	quit = 0
	song_state = listener.get_current_song_uri()
	

	# Start timers
	check_song_change([listener, song_state])
	save_song_graph([listener])
	
	while quit < 1:
		inp = input("Search for a song to add it to your queue: ")
		try:
			if inp[0] == '_':
				# Process a command
				command_switchboard(inp[1:], listener, song_state)
			else:
				r = listener.process_and_add(inp)
				if r == 0:
					print("Sorry, couldn't add that song - try searching again")
		except IndexError:
			# Just pressing enter should reset the scheme
			continue

def initialise():
	sp = sapi.create_sp()
	device_id = sapi.choose_device(sp)
	listen = listener(sp, device_id)
	return listen

def main():
	listen = initialise()
	listen_along_dj(listen)

if __name__ == '__main__':
	main()
