import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import pickle


class listener:
	def __init__(self, sp, device_id):
		self.device_id = device_id
		self.sp = sp
		self.song_graph = self.load_graph()
		self.queue  = []

	def play_track(self, track_uri):
		'''
		Takes in a song_uri and plays it
		'''
		self.sp.start_playback(device_id=self.device_id,uris=[track_uri])

	def clear_queue(self):
		'''
		Clears the current song queue
		'''
		

	def queue_track(self, track_uri):
		'''
		Queuing function for playback without listening
		'''
		self.sp.add_to_queue(track_uri, self.device_id)		
	
	def load_graph(self):
		'''
		Loads the current copy of the song graph
		'''
		try:
			with open('disk/song_map.pickle', 'rb') as fd:
				graph = pickle.load(fd)
			return graph
		except:
			# If a current copy doesn't exist, just return an empty
			return {}

	def write_graph(self):
		'''
		Writes a current copy of the song graph as a pickle file
		'''
		with open('disk/song_map.pickle', 'wb') as fd:
			pickle.dump(self.song_graph, fd)

	def add_to_queue(self, track_uri):
		'''
		Given a song, add it to the queue
		'''
		self.sp.add_to_queue(track_uri, self.device_id)
		self.queue.append(track_uri)

	def skip_song(self):
		'''
		Skips to the next song
		'''
		self.sp.next_track(self.device_id)

	def search_song(self, search_str):
		'''
		Searches a song, returns the song record. Returns None on failure
		'''
		res = self.sp.search(search_str)
		try:
			return res['tracks']['items'][0]
		except:
			return 0

	def get_current_song_uri(self):
		'''
		Returns the uri of the song that's currently playing
		'''
		res = self.sp.current_user_playing_track()
		song_uri = res['item']['uri']
		return song_uri
		
	def update_graph(self, current_song):
		'''
		Creates links between the current song, and songs added in the queue
		Should be called at some well defined interval. For now we'll make it manual
		In future it is run on song changeover
		'''

		root = current_song
		vertices = [root] + [leaf for leaf in self.queue]
		
		for i in vertices:
			for j in vertices:
				if i == j:
					continue
				
				if i in self.song_graph:
					if j not in self.song_graph[i]:
						self.song_graph[i].append(j)
				else:
					self.song_graph[i] = [j]

		# Clear the current queue
		self.queue = []	

		
	def process_and_add(self, search_str):
		'''
		Manages the end-to-end process of searching a song and getting it played
		'''
		song_record = self.search_song(search_str)

		# Failed searches return None
		if song_record == 0:
			return 0
		
		# Code to add to the graph goes here

		self.add_to_queue(song_record['uri'])
		
		# Echo the song name and artist to console //todo
		song_name = song_record['name']
		song_artist = song_record['album']['artists'][0]['name']
		print("Added " + song_name + " - " + song_artist + " to the queue!")
		return 1

	def listen(self):
		print("I'm listening!")
		pprint(self.song_graph)
			

if __name__ == '__main__':
	
	# Authorise
	scope = 'user-read-playback-state,user-modify-playback-state'
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))

	# Get kanga's device id
	device_id = get_device_by_name('kanga', sp)


	# Initialise the listener
	listen = listener(sp)
	listen.listen()
	
