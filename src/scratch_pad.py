import pandas as pd
from matplotlib import pyplot
import matplotlib.pyplot as plt
import itertools
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
from importlib import reload
import src.vehicle_trajectory as lib
idx = pd.IndexSlice

# sample data
#trip_id,start_date,route_id,train_id,direction,current_stop_sequence,current_status,timestamp,stop_id,message_timestamp
# 096700_1..N03R,20191120,1,01 1607  SFT/242,1,38,1,1574287365,101N,1574287432
#096700_1..N03R,20191120,1,01 1607  SFT/242,1,38,1,1574287365,101N,1574287432

# get a trip with at least 68 updates (that is the most number of updates we've seen)
# fixed auto indent feature: https://github.com/ipython/ipython/issues/11257
reload(lib)
fname = 'data/raw/realtime/stream.csv'
f = lib.load_data(fname)

route = "1"
direction = 1
trip_ids = f.loc[idx[route, direction, :, :, :]].index.get_level_values(0).unique()
trip_ids

longest = lib.longest_trip(f, route, direction)

trip_ids[1]

journey = f.loc[idx['1', 1, longest, :, :]]
journey = journey[journey.current_status != 2]
journey = journey.sort_index(level='timestamp')
plt.plot(journey.index.get_level_values(1), journey.stop_name)


# can probably do sort all at once
for i in trip_ids:
	journey = f.loc[idx['1', 1, i, :, :]]
	journey = journey[journey.current_status != 2]
	journey = journey.sort_index(level='timestamp')
	plt.plot(journey.index.get_level_values(1), journey.stop_name)

journey.index.format(formatter=lambda x: x[1])

plt.
journey.index
stops.loc['110N']
journey.set_index('stop_id')
longest = lib.longest_trip(f, "1", 1)
longest
f.head(2).index
d = f.loc[idx['1', 1, longest, :, :]]
plt.plot(
d.timestamp
d.stop_id
plt.plot(d.timestamp, d.stop_id)
f.head(10)
cla()

journey.index.get_level_values(1)

reload(lib)
route = "1"
direction = 1

trip_ids = f.loc[idx[route, direction, :, :, :]].index.get_level_values(0).unique()
for i in trip_ids:
	print(i)

trip_ids = pd.unique(f.loc[idx[route, direction, :, :, :]].trip_id)
all_stops = lib.all_stops(f, route, direction)
fig, ax = plt.subplots()
for ti in trip_ids:
	trip_data = f.loc[idx[route, direction, ti, :, :], :]
	lib.plot_trip(trip_data, all_stops, ax)

plot_trip(trip_ids[3])
pyplot.cla()
# the status codes
#statuses = ['incoming', 'stopped', 'in transit']	
#f[f.trip_id == trip_id].groupby(['stop_id', 'current_status']).size().head(10)
's'*range(5)

d = pd.DataFrame(data={'x': range(5), 'y': ['s1', 's1', 's2', 's3', 's4']})
d.y
d.index
d.y

plt.plot(range(5), d.y)
