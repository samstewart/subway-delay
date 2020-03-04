import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
idx = pd.IndexSlice

def load_data(fname):
	"""
	Loads the bluetooth data, converts unix timestamps to propert datetimes, and attaches the stop meta data (such as stop_name and geolocation). In our current structure, choose fname = 'data/raw/realtime/stream.csv'. 

	vehicle.trip.tripId,vehicle.trip.startDate,vehicle.trip.routeId,vehicle.trip.[nyctTripDescriptor].trainId,vehicle.trip.[nyctTripDescriptor].direction,vehicle.currentStopSequence,vehicle.currentStatus,vehicle.timestamp,vehicle.stopId,stop_name,header.timestamp
	"""
	f = pd.read_csv(fname, parse_dates=['vehicle.timestamp', 'header.timestamp'], date_parser=lambda col: pd.to_datetime(pd.to_numeric(col), unit='s')) 
	f = f.set_index(['vehicle.trip.routeId', 'vehicle.trip.[nyctTripDescriptor].direction', 'vehicle.trip.tripId', 'stop_name', 'vehicle.timestamp'])
	
	# get rid of the duplicates
	f = f.loc[~f.index.duplicated(keep='first')]

	# add the stop metadata (like geoloc and name)
	f = f.sort_index(level=['vehicle.trip.tripId', 'vehicle.timestamp'])

	return f

# design question: should we track parameters as input or focus on making stuff chainable and passing in the data? here we have to pass through the arguments instead of just passing the data. results in recomputing data and copying parameters. On the other hand, we need to ensure the data has a particular index (should have only three features) and this means we need to guarantee the output of trips_for_route_and_direction
def longest_trips(data, route, direction, n):
	"""returns the trip ID of the 'n' longest trips as measured by number of events. Useful for finding the correct ordering of stops or for plotting a single trajectory"""
	number_of_times = data.loc[idx[route, direction, :, :, :]].groupby('trip_id').size()
	return number_of_times.nlargest(n)

def plot_trip(d, route, direction, trip_id):
	"""Plots a single trips as stop names against arrival time (this should plot an increasing function with dots at the sensor readings). Ignores status updates of 'departed' = 2 since unreliable"""
	journey = d.loc[idx[route, direction, trip_id, :, :]]
	journey = journey[journey.current_status != 2] # ignore the departing signals
	# plot stop names against timestamps of sensor events (incoming, stopped)
	plt.plot(journey.index.get_level_values(1), journey.stop_name)

	#journey.plot(x='timestamp', y='stop_id', marker='o', markersize=2, ax=ax, legend=False)

