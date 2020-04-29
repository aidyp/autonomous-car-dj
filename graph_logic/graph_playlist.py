'''
The aim here is to generate a playlist 'walk' along a user graph
'''
import random
import pickle

SNAPBACK = 3


sample_disjoint_graph = {'A':['B','C'],
                         'B':['A','C'],
                         'C':['B','C'],
                         'D':['E','F'],
                         'E':['D','F'],
                         'F':['D','E']}

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
	'''
	Does a depth first walk up to some pre defined length

	TODO: If it finishes a chain it seems to jump to another one
	'''
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


def bfs_adjusted(graph, node, visited, length):
	'''
	Does a breadth first walk up to some pre-defined length
	'''
	queue = []

	visited.append(node)
	queue.append(node)

	while queue:
		s = queue.pop(0)
		neighbours = graph[s]
		random.shuffle(neighbours) # Shuffle neighbours for some variance
		for neighbour in neighbours:
			if len(visited) == length:
				# Stop the walk
				return
			if neighbour not in visited:
				visited.append(neighbour)
				queue.append(neighbour)


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

def generate_playlist(first_song, song_graph, length):
	'''
	Given a song graph, returns a playlist that is a walk along the graph
	'''
	if first_song == None:
        	v = get_vertices(song_graph)
        	root = pick_first_song(v)
	else:
		root = first_song

	# Generate a playlist
	playlist = walk_graph(root, song_graph, length)

	return playlist

def tests():
	visited = walk_graph('D', sample_disjoint_graph, 5)
	print(visited)




if __name__ == '__main__':
	tests()
