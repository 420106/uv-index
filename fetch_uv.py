import requests
import json
import sys
import os


def map_coords(loc):
	loc = loc.lower()
	coords = {
		'sydney': (-33.865143, 151.2099),
		'melbourne': (-37.8136, 144.9631),
		'brisbane': (-27.4698, 153.0251)
	}

	if loc not in coords:
		raise KeyError(f'We have not collected the coordinates of {loc.title()} yet.')

	return coords[loc]


def fetch_uv(coords, api_key):

	lat, lng = coords
	url = f'https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}'
	headers = {'x-access-token': api_key}

	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		return response.json()['result']
	else:
		print(f'Error: {response.status_code} - {response.text}')


def save_data(data, loc, mode='local', path='raw_data'):
	loc = loc.lower()
	if mode == 'local':
		folder = os.path.join(path, loc)
		if os.path.exists(folder) == False:
			os.mkdir(folder)
		ts = data['uv_time'].replace('-', '').replace(':', '')
		file_name = f'{loc}-{ts}.json'
		with open(os.path.join(folder, file_name), 'w+') as file:
			json.dump(data, file)


if __name__ == '__main__':
	
	if os.environ.get('ENVIRONMENT') == 'dev':
		import config_dev

	loc = sys.argv[1]
	openuv_api_key = os.environ.get('OPENUV_API_KEY')

	coords = map_coords(loc)
	data = fetch_uv(coords, openuv_api_key)
	save_data(data, loc)