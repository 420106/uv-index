import pytest
import json
import py
import os
import fetch_uv as script


@pytest.fixture
def data():
	data = json.loads('''
		{
		   "uv":0,
		   "uv_time":"2023-03-15T12:18:50.276Z",
		   "uv_max":8.2768,
		   "uv_max_time":"2023-03-15T02:30:42.195Z",
		   "ozone":268.4,
		   "ozone_time":"2023-03-15T12:04:39.156Z",
		   "safe_exposure_time":{
		      "st1":null,
		      "st2":null,
		      "st3":null,
		      "st4":null,
		      "st5":null,
		      "st6":null
		   },
		   "sun_info":{
		      "sun_times":{
		         "solarNoon":"2023-03-15T02:30:42.195Z",
		         "nadir":"2023-03-14T14:30:42.195Z",
		         "sunrise":"2023-03-14T20:18:53.427Z",
		         "sunset":"2023-03-15T08:42:30.963Z",
		         "sunriseEnd":"2023-03-14T20:21:35.650Z",
		         "sunsetStart":"2023-03-15T08:39:48.740Z",
		         "dawn":"2023-03-14T19:52:35.486Z",
		         "dusk":"2023-03-15T09:08:48.904Z",
		         "nauticalDawn":"2023-03-14T19:21:42.726Z",
		         "nauticalDusk":"2023-03-15T09:39:41.664Z",
		         "nightEnd":"2023-03-14T18:50:12.192Z",
		         "night":"2023-03-15T10:11:12.198Z",
		         "goldenHourEnd":"2023-03-14T20:53:30.265Z",
		         "goldenHour":"2023-03-15T08:07:54.125Z"
		      },
		      "sun_position":{
		         "azimuth":0.7792127310436628,
		         "altitude":-0.6942382261809107
		      }
		   }
		}
		''')

	return data


@pytest.fixture
def tmpdir(tmpdir):
	return tmpdir


def test_map_coords_with_valid_location():
	assert (-37.8136, 144.9631) == script.map_coords('Melbourne')


def test_map_coords_with_invalid_location():
	with pytest.raises(KeyError):
		script.map_coords('Gotham City')


@pytest.mark.skip('API test')
@pytest.mark.parametrize('key', [
		'uv',
		'uv_time',
		'uv_max',
		'uv_max_time'
	])
def test_api(key):
	# test validity of the api key and api endpoint
	if os.environ.get('ENVIRONMENT') == 'dev':
		import config_dev
	openuv_api_key = os.environ.get('OPENUV_API_KEY')
	data = script.fetch_uv((-37.8136, 144.9631) , openuv_api_key)
	assert None != data
	# test data structure
	assert key in data


def test_save_data_in_local_mode(data, tmpdir):
	script.save_data(data, 'Melbourne', mode='local', path=tmpdir)
	# test file name and path
	assert 'melbourne-20230315T121850.276Z.json' in os.listdir(os.path.join(tmpdir, 'melbourne'))