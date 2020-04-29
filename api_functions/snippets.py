'''
Contains snippets that I'm going to need to deploy and integrate later
'''

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import json





# *********************** #
# Snippet 1 | Play a Song #
# *********************** #


scope = 'user-read-playback-state,user-modify-playback-state'
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))

# Shows playing devices
res = sp.devices()
pprint(res)


# Change track, given a device_id and a uri
def play_track(song):
	# Given a song json record, play it
	song_uri = song['uri']
	sp.start_playback(device_id='9f64c479693a0f221a0dabbf9395592be9ffb2f6',uris=[song_uri])


# *********************** #
# Snippet 2 | Search Song #
# *********************** #

def search_song(search_str):
	'''
	Searches for a song, function returns the json record of the top result
	'''
	res = sp.search(search_str)
	return res['tracks']['items'][0]


# *********************** #
# Snippet 3 | Add Song    #
# *********************** #

def add_track_to_queue(device_id, song):
	song_uri = song['uri']
	sp.add_to_queue(song_uri, device_id)


next_song = search_song('the difference flume')
#pprint(next_song)
#add_track_to_queue('9f64c479693a0f221a0dabbf9395592be9ffb2f6', next_song)

# *********************** #
# Snippet 4 | Graph Song  #
# *********************** #

# Traditional python graph is a dictionary with nodes as keys #



def add_to_graph(x, y , graph):
	# Songs are added in a pair (x, y), by uri 
	if x in graph:
		graph[x].append(y)
	else:
		graph[x] = [y]

	if y in graph:
		graph[y].append(x)
	else:
		graph[y] = [x]

def link_songs():
	'''
	Builds a song graph out of linked song titles from a csv. 
	Bit crap but okay as a first solution
	'''
	

def song_graphs():
	# URI is unique so we can use it to map a song to the song record returned
	song_map = {}
	
	# Similarly, track URI by song graph
	song_graph = {}

	song_x = search_song('jazz we\'ve got')
	song_y = search_song('rebirth of slick')

	print(song_graph)
	add_to_graph(song_x['uri'], song_y['uri'], song_graph)
	print(song_graph)
	song_z = search_song('what am i to do')
	add_to_graph(song_x['uri'], song_z['uri'], song_graph)
	print(song_graph)

song_graphs()

