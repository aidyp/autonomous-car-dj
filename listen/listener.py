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
		self.song_cache = {'ADDED':[]}

	def play_track(self, track_uri):
		'''
		Takes in a song_uri and plays it
		'''
		self.sp.start_playback(device_id=self.device_id,uris=[track_uri])

	def add_to_cache(self, song_record):
		'''
		Adds the most recent song record to the cache. Cache remembers the last ten songs
		'''
		# To do
		song_uri = song_record['uri']

		# Add to cache if not already in it
		if song_uri not in self.song_cache:
			self.song_cache['ADDED'].append(song_uri)
			self.song_cache[song_uri] = song_record


		# Trim the cache if it's too long
		if len(self.song_cache['ADDED']) > 10:
			# pops the first entry from the cache
			to_delete = self.song_cache['ADDED'].pop(0)
			del self.song_cache[to_delete]

	def get_song_record_by_uri(self, song_uri):
		'''
		Returns a full song record by the song_uri
		'''

		# Check if it's in the cache
		try:
			record = self.song_cache[song_uri]
		except:
			record = self.sp.track(song_uri)

		# If it's not in the cache, will have to search for it
		if record == None:
			return None
		return record

	def clear_spotify_queue(self):
		'''
		Clears the current song queue. Doesn't work ):
		'''
		# Turns out the spotify API has no clean way of doing this, the best trick is to
		# 1) find a playlist that has exactly zero songs
		# 2) play it
		# 3) skip it
		wipe = 'spotify:track:5sKN6nGLcbfveIVEoejeoC'
		print("Trying to clear the queue")
		self.sp.start_playback(device_id=self.device_id, uris=[wipe])


	def pop_queue(self):
		'''
		Removes the last track from the mapping queue
		Echoes the song removed (for now)
		'''
		removed = self.queue.pop()
		song_record = self.song_cache[removed]
		to_print = self.pretty_name(song_record)
		print(to_print + " removed from the adding queue (but not the song queue)")


	def queue_track(self, track_uri):
		'''
		Queuing function for playback without listening
		'''
		self.sp.add_to_queue(track_uri, self.device_id)
		#self.add_to_cache(self.get_song_record_by_uri(track_uri))

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

	def get_graph(self):
		'''
		Returns a reference to the graph object
		'''
		return self.song_graph

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
			song_record = res['tracks']['items'][0]

			# Cache the record before returning
			self.add_to_cache(song_record)

			return song_record
		except:
			return None

	def get_current_song_uri(self):
		'''
		Returns the uri of the song that's currently playing
		Extend to return the pretty name as well
		'''
		res = self.sp.current_user_playing_track()
		song_uri = res['item']['uri']
		return song_uri
	def get_spotify_queue(self):
		'''
		Returns the current user's music queue as a list
		'''
		pass

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

	def pretty_name(self, song_record):
		'''
		Gets the nice name for a song from the record
		'''
		song_name = song_record['name']
		song_artist = song_record['album']['artists'][0]['name']
		return (song_name + ' - ' + song_artist)
	def pretty_name_by_uri(self, uri):
		'''
		Gets the nice name from the uri
		'''
		record = self.get_song_record_by_uri(uri)
		return self.pretty_name(record)
		
	def process_and_add(self, search_str):
		'''
		Manages the end-to-end process of searching a song and getting it played
		'''
		song_record = self.search_song(search_str)

		# Failed searches return None
		if song_record == 0:
			return 0

		# Add to the song queue
		self.add_to_queue(song_record['uri'])


		# Echo the song name and artist to console
		to_print = self.pretty_name(song_record)
		print("Added " + to_print + " to the queue!")
		return 1


if __name__ == '__main__':

	# Authorise
	scope = 'user-read-playback-state,user-modify-playback-state'
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,username='jokezfish'))

	# Get kanga's device id
	device_id = get_device_by_name('kanga', sp)


	# Initialise the listener
	listen = listener(sp)
	listen.listen()
