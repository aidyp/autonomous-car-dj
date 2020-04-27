import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = 'user-read-playback-state,user-modify-playback-state'

def create_sp():
	sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=SCOPE,username='jokezfish'))
	return sp

def choose_device(sp):
	'''
	Let's the user choose the device they want to play on 
	'''
	devices = sp.devices()
	device_map = {}
	device_list = devices['devices']
	for i in range(0, len(device_list)):
		print(str(i) + ") " + str(device_list[i]['name']))
		device_map[i] = device_list[i]['name']

	device_id = None
	while device_id == None:
		inp = input("Choose device by number: ")
		device_id = get_device_by_name(device_map[i], devices)
	
	return device_id


def get_device_by_name(device_name, devices):
	'''
	Gets device id by device name. Device must be active on spotify
	'''

	for device in devices['devices']:
		if device['name'] == device_name:
			return device['id']
	return None
