'''
The aim here is to generate a playlist 'walk' along a user graph
'''
import random


def load_graph():
	with open('../disk/song_map.pickle'. 'rb') as fd:
		graph = pickle.load(fd)
	return graph


def get_vertices(graph):
	'''
	Returns a list of vertices in case they're needed
	'''
	return [k for k in graph.keys()]


def pick_first_song(vertices):
	'''
	Give a list vertices, picks a random element
	'''
	

