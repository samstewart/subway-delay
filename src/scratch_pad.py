import pandas as pd
from time import sleep
from matplotlib import pyplot
import numpy as np
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

plt.figure()
plt.cla()

f = f[f.current_status != 2]

# want to find guy who hits the most number of stops
journey.index
aggregate(lambda rows: rows.index.get_level_values(1).shape[0])

longest
longest = lib.longest_trip(f, '1', 1)
f.index.get_level_values(3).
f.index.names
journey.index.get_level_values(0).unique().shape[0]
f.drop

# appears to be able to get longest trip (unique stops). not sure if any different than what we had before
trip_lengths = f.loc[idx["1", 1, :, :, :]].groupby(level='trip_id').apply(lambda t: t.index.unique().get_level_values(0).shape[0])


trip_lengths[longest]
longest = trip_lengths.nlargest(10)

trip_lengths.max()
longest
journey.index.get_level_values(1)
extras = np.array(['231 St', '238 St', 'Van Cortlandt Park - 242 St'])
extras2 = np.array(['Rector St', 'South Ferry'])
stations = np.concatenate((extras2, stations))
stations = np.concatenate((stations[0:2], stations[3:]))
stations = np.concatenate((extras2, journey.stop_name.unique(), extras))
stations
longest = lib.longest_trip(f, "1", 1)

journey = f.loc[idx["1", 1, ti1, :, :]]
journey

journey.tail(1)

journey.index.get_level_values(1)

stations
pd.CategoricalDtype(stations, ordered=True)
stations
# can deduce this from the data
times = pd.date_range(start='2020-01-07 00:20:00', end='2020-01-07 01:10:00', periods=len(stations))

# dammit we have to convert the categorical into numerical, annoying. actually I think it was my error?
plt.cla()
stations
plt.yticks(stations)
# constant speed


ti = ['112400_1..N03R', '112400_1..N', '120000_1..N03R']

problem_id = '112400_1..N'
f.loc[idx['1', 1, ti[1], :, :]].stop_name

l = list(trip_ids.array)
l = ti 

plt.cla()
plt.plot(times, stations, linestyle='--')
for i in l:
	lib.plot_trip(f, '1', 1, i)

plt.legend(['baseline'] + l)



plt.yticks(stations)


reload(lib)
# can probably do sort all at once
for i in trip_ids:
	lib.plot_trip(f, '1', 1, i)	

ti2
ti1
ti2 = '114200_1..N03R'
plt.legend(trip_ids)
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


ti1 = '118150_1..N03R'

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
