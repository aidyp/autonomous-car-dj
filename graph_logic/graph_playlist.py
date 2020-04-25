'''
The aim here is to generate a playlist 'walk' along a user graph
'''
import random
import pickle

SNAPBACK = 3


sample_graph = {'A':['B', 'C'],
                'B':['A', 'C', 'D', 'E'],
                'C':['A', 'B', 'F'],
                'D':['B', 'E'],
                'E':['B', 'D'],
                'F':['C']}


def load_graph():
	with open('../disk/song_map.pickle', 'rb') as fd:
		graph = pickle.load(fd)
	return graph


def get_vertices(graph):
	'''
	Returns a list of vertices in case they're needed
	'''
	return [k for k in graph.keys()]

def dfs_adjusted(graph, node, visited, length):

	if len(visited) == length:
		# Stop the walk
		return

	if node not in visited:
		visited.append(node)
		neighbours = graph[node]
		# shuffle neighbours for some variance
		random.shuffle(neighbours)
		for neighbour in neighbours:

			# Need to think where to add snapback			
			dfs_adjusted(graph, neighbour, visited, length)
		
def pick_first_song(vertices):
	'''
	Give a list vertices, picks a random element
	'''
	root = random.randint(0, len(vertices) - 1)
	return vertices[root]

def walk_graph(root, song_graph, length):
	visited = []
	dfs_adjusted(song_graph, root, visited, length)
	return visited

def generate_playlist(song_graph, length):
	'''
	Given a song graph, returns a playlist that is a walk along the graph
	'''
	
	# Pick the first song
	v = get_vertices(song_graph)
	root = pick_first_song(v)

	# Generate a playlist
	playlist = walk_graph(root, song_graph, length)
	
	return playlist

	
	

