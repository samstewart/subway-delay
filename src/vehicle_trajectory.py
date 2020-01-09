import pandas as pd
from pandas.api.types import CategoricalDtype
idx = pd.IndexSlice

def load_data(fname):
	f = pd.read_csv(fname, parse_dates=['timestamp', 'message_timestamp'], date_parser=lambda col: pd.to_datetime(pd.to_numeric(col), unit='s'), index_col=['route_id', 'direction', 'trip_id', 'stop_id', 'timestamp'])

	f = f.drop_duplicates()
	
	# add the stop metadata (like geoloc and name)
	stops = pd.read_csv('data/raw/static_transit/stops.txt', index_col='stop_id')
	f = f.join(stops) 

	return f

# design question: should we track parameters as input or focus on making stuff chainable and passing in the data? here we have to pass through the arguments instead of just passing the data. results in recomputing data and copying parameters. On the other hand, we need to ensure the data has a particular index (should have only three features) and this means we need to guarantee the output of trips_for_route_and_direction
def longest_trip(data, route, direction):	
	"""returns the trip ID of one of the longest trips"""
	number_of_times = data.loc[idx[route, direction, :, :, :]].groupby(level=0).size()
	return number_of_times.index[number_of_times >= number_of_times.max()][0]

# should only be run once per route. Can deduce the list of stops from the data
def all_stops(data, route, direction):
	return CategoricalDtype(categories=pd.unique(data.loc[idx[route, direction, longest_trip(data, route, direction), :, :]].stop_id), ordered=True)

def plot_trip(trip_data, all_stops, ax=None):
	journey = trip_data[trip_data.current_status != 2].copy()
	#journey.timestamp = journey.timestamp - journey.head(1).timestamp[0]
	journey.stop_id = journey.stop_id.astype(all_stops).cat.codes
	journey.plot(x='timestamp', y='stop_id', marker='o', markersize=2, ax=ax, legend=False)

	

