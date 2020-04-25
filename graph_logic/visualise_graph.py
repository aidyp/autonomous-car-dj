'''
Going to have some way to visualise the music map you have
'''
import plotly.graph_objects as go
import networkx as nx
from netwulf import visualize
import pickle
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


sample_graph = {'A':['B', 'C'],
                'B':['A', 'C', 'D', 'E'],
                'C':['A', 'B', 'F'],
                'D':['B', 'E'],
                'E':['B', 'D'],
                'F':['C']}


# Initialise a spotipy object
scope = 'user-read-playback-state,user-modify-playback-state'
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))

def load_song_graph():
	with open('../disk/song_map.pickle', 'rb') as fd:
		graph = pickle.load(fd)
	return graph

def get_pretty_name_by_uri(song_uri):
	song = sp.track(song_uri)
	song_name = song['name']
	song_artist = song['album']['artists'][0]['name']
	return song_name + ' - ' + song_artist


def create_uri_mapping(mapping, song_graph):
	'''
	Pass in an empty mapping dictionary,
	returns a mapping from URI -> song name for prettier visualisation
	'''
	for song_uri in song_graph.keys():
		pretty_name = get_pretty_name_by_uri(song_uri)
		mapping[song_uri] = pretty_name
		

def visualise_song_graph():
	
	# Make the pretty song map
	song_graph = load_song_graph()
	uri_map = {}
	create_uri_mapping(uri_map, song_graph)
	
	# Transform the graph
	G = nx.Graph(song_graph)
	H = nx.relabel_nodes(G, uri_map)

	# Visualise
	visualize(H)
		
def main():
	visualise_song_graph()
	
if __name__ == '__main__':
	main()	

	

