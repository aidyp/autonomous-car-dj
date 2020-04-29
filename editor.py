#!/usr/bin/env python3

import pickle
from listen.listener import listener
from api_functions.misc_functions import create_sp
from graph_logic.visualise_graph import visualise_song_graph



class graph_editor:
	def __init__(self, song_graph):
		self.song_graph = song_graph
		# If no song graph is passed, automatically loads it
		if self.song_graph == None:
			self.song_graph = load_graph()

	def load_graph(self):
		with open('disk/song_map.pickle', 'rb') as fd:
			graph = pickle.load(fd)
		return graph
	def print_graph(self):
		print(self.song_graph)

	def delete_song(self, song_uri):
		'''
		Deletes a song from the graph given its uri
		'''
		if song_uri in self.song_graph:
			edges = self.song_graph[song_uri]
		else:
			# Can't delete a song that's not there
			return

		for edge in edges:
			# I'm on the edge of glory!
			self.song_graph[edge].remove(song_uri)

		del self.song_graph[song_uri]

	def delete_link(self, uri_a, uri_b):
		'''
		Removes a link between two songs
		'''
		try:
			self.song_graph[uri_a].remove(uri_b)
			self.song_graph[uri_b].remove(uri_a)
		except:
			# Exception will trigger when trying to delete a uri that's not there
			pass

	def mesh_link(self, songs):
		'''
		If you want to mesh a group of songs
		'''
		for i in range(0, len(songs)):
			for j in range(0, len(songs)):
				if i == j:
					continue
				add_link(songs[i], songs[j]) # A little lazy but it will do the job

	def add_link(self, uri_a, uri_b):
		'''
		Adds a link between two songs.
		'''
		if (uri_a in self.song_graph) and (uri_b in self.song_graph):
		# Case 1, both songs are already in the graph
		# Add a link if it doesn't already exist
			if uri_b not in self.song_graph[uri_a]:
				self.song_graph[uri_a].append(uri_b)
				self.song_graph[uri_b].append(uri_a)
		elif (uri_a in self.song_graph):
			# Case 2, song a is already in the graph
			if uri_b not in self.song_graph[uri_a]:
				self.song_graph[uri_a].append(uri_b)
				self.song_graph[uri_b] = [uri_a]
		elif (uri_b in self.song_graph):
			# Case 3, song b is already in the graph
			if uri_a not in self.song_graph[uri_b]:
				self.song_graph[uri_b].append(uri_a)
				self.song_graph[uri_a] = [uri_b]
			else:
			# Case 4, none of the songs are in the graph
				self.song_graph[uri_a] = [uri_b]
				self.song_graph[uri_b] = [uri_a]

	def get_all_uris(self):
		'''
		Gets a list of the uris
		'''
		return [song_uri for song_uri in self.song_graph.keys()]

	def visualise(self, mapping):
		visualise_song_graph(self.song_graph, mapping)


def okay_to_continue():
	inp = input("Okay to continue? (y/n): ")
	if inp == 'y':
		return True
	return False

def get_uri_name(songs, listener):
	'''
	Takes in a list of search terms, returns their
	uri and pretty name for echoing to username
	'''
	uri_name = []
	for song in songs:
		song_record = listener.search_song(song)

		# Check something was returned
		if song_record == None:
			return None

		song_name = listener.pretty_name(song_record)
		song_uri = song_record['uri']
		uri_name.append([song_uri, song_name])

	# Check correctness
	for elem in uri_name:
		print(elem[1])
	if okay_to_continue() == False:
		return None

	return uri_name

def link(body, listener, graph_editor):
	songs = body.split(';')

	# For each song, get the URI (and song name to double check)
	uri_name = get_uri_name(songs, listener)

	# Error checking
	if uri_name == None:
		return None

	# Mesh link the uris
	uris = [x[0] for x in uri_name]
	graph_editor.mesh_link(uris)

def unlink(body, listener, graph_editor):
	songs = body.split(';')

	# For each song, get the URI (and song name to double check)
	uri_name = get_uri_name(songs, listener)

	# Error checking
	if uri_name == None:
		return None

	# unlink the uris
	uris = [x[0] for x in uri_name]
	graph_editor.delete_link(uris[0], uris[1])

def delete(body, listener, graph_editor):
	song = body

	# Get uri and song name
	uri_name = get_uri_name([song], listener)

	# Error checking
	if uri_name == None:
		return None
	uri = uri_name[0][0]
	graph_editor.delete_song(uri)

def save_changes(listener):
	listener.write_graph()

def show_network(listener, graph_editor):
	'''
	Calls the visualiser functionality, this is blocking
	'''
	# Make the uri map
	uris = graph_editor.get_all_uris()
	mapping = {}
	for uri in uris:
		song_record = listener.get_song_record_by_uri(uri)
		full_name = listener.pretty_name(song_record)
		mapping[uri] = full_name
	graph_editor.visualise(mapping)

def command_parse(user_input, listener, graph_editor):
	# Split the command
	cmd,space,body = user_input.partition(" ")

	if cmd == 'link':
		# Link n songs in the body
		link(body, listener, graph_editor)
	elif cmd == 'unlink':
		# unlink 2 songs in the graph
		unlink(body, listener, graph_editor)
	elif cmd == 'delete':
		# deletes a song in the graph
		delete(body, listener, graph_editor)
	elif cmd == 'save':
		# Saves the changes
		save_changes(listener, graph_editor)
	elif cmd == 'visualise':
		# Loads the visualiser (note this is blocking!)
		# Don't use yet, need to restructur the visualiser
		show_network(listener, graph_editor)
	elif cmd == 'quit':
		return False
	return True


def control_loop(listener, graph_editor):
	
	inp = input("Enter your command: ")
	command_parse(inp, listener, graph_editor)

def initialise():

	# Get a listener object
	sp = create_sp()
	listen = listener(sp, None)

	# Get the song graph from the listener
	song_graph = listen.get_graph()

	# Initialise the graph editor
	graph_edit = graph_editor(song_graph)
	rep = True
	while rep:
		rep = control_loop(listen, graph_edit)


def main():
	initialise()

if __name__ == '__main__':
	main()
