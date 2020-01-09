import pandas as pd
from pandas.api.types import CategoricalDtype
idx = pd.IndexSlice

def load_data(fname):
	"""
	Loads the bluetooth data, converts unix timestamps to propert datetimes, and attaches the stop meta data (such as stop_name and geolocation). In our current structure, choose fname = 'data/raw/realtime/stream.csv'. 
	"""
	f = pd.read_csv(fname, parse_dates=['timestamp', 'message_timestamp'], date_parser=lambda col: pd.to_datetime(pd.to_numeric(col), unit='s'), index_col=['route_id', 'direction', 'trip_id', 'stop_id', 'timestamp'])

	f = f.drop_duplicates()
	
	# add the stop metadata (like geoloc and name)
	stops = pd.read_csv('data/raw/static_transit/stops.txt', index_col='stop_id')
	f = f.join(stops) 

	return f

# design question: should we track parameters as input or focus on making stuff chainable and passing in the data? here we have to pass through the arguments instead of just passing the data. results in recomputing data and copying parameters. On the other hand, we need to ensure the data has a particular index (should have only three features) and this means we need to guarantee the output of trips_for_route_and_direction
def longest_trip(data, route, direction):	
	"""returns the trip ID of one of the longest trips as measured by number of stops. Useful for finding the correct ordering of stops or for plotting a single trajectory"""
	number_of_times = data.loc[idx[route, direction, :, :, :]].groupby(level=0).size()
	return number_of_times.index[number_of_times >= number_of_times.max()][0]

def plot_trip(d, route, direction, trip_id, ax=None):
	"""Plots a single trips as stop names against arrival time (this should plot an increasing function with dots at the sensor readings). Ignores status updates of 'departed' = 2 since unreliable"""
	journey = d.loc[idx[route, direction, trip_id, :, :]]
	journey = journey[journey.current_status != 2] # ignore those sensor readings of 'departed'
	journey.plot(x='timestamp', y='stop_id', marker='o', markersize=2, ax=ax, legend=False)

