def get_device_by_name(device_name, sp):
	'''
	Gets device id by device name. Device must be active on spotify
	'''

	devices = sp.devices()
	for device in devices['devices']:
		if device['name'] == device_name:
			return device['id']
	return None
