
def plot_trip(d, route, direction, trip_id):
	"""Plots a single trips as stop names against arrival time (this should plot an increasing function with dots at the sensor readings). Ignores status updates of 'departed' = 2 since unreliable"""
	journey = d.loc[idx[route, direction, trip_id, :, :]]
	journey = journey[journey.current_status != 2] # ignore the departing signals
	# plot stop names against timestamps of sensor events (incoming, stopped)
	plt.plot(journey.index.get_level_values(1), journey.stop_name)

	#journey.plot(x='timestamp', y='stop_id', marker='o', markersize=2, ax=ax, legend=False)

