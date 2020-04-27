'''
Some helper functions to edit connections, delete songs, add connections manually to one's music graph
'''

import pickle

def load_graph():
	with open('../disk/song_map.pickle', 'rb') as fd:
		graph = pickle.load(fd)
	return graph

def delete_song(song_uri, song_graph):
	'''
	Deletes a song from the graph given its uri
	'''
	edges = song_graph[song_uri]
	
	for edge in edges:
		# I'm on the edge of glory!
		song_graph[edge].remove(song_uri)
	
	del song_graph[song_uri]

def delete_link(uri_a, uri_b, song_graph):
	'''
	Removes a link between two songs
	'''
	try:
		song_graph[uri_a].remove(uri_b)
		song_graph[uri_b].remove(uri_a)
	except:
		# Exception will trigger when trying to delete a uri that's not there
		pass

def add_link(uri_a, uri_b, song_graph):
	'''
	Adds a link between two songs.
	'''
	
	


	
	

