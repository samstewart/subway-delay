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
reload(lib)
d = lib.load_data('data/raw/realtime/stream.csv')

# change these to plot different routes and directions
route = "1"
direction = 1
n = 10

first_reading = d.loc[idx[route, direction, :, :, :]].head(1).index.get_level_values('timestamp')[0]
last_reading = d.loc[idx[route, direction, :, :, :]].tail(1).index.get_level_values('timestamp')[0]
# can deduce this from the data
# ideally route would a string key, but it is choosing integer instead
# kind of inefficient to reload this everytime, should we pass it in?
stations = pd.read_csv('data/raw/static_transit/route_stops.csv', index_col=['route', 'direction', 'stop_index']).loc[idx[int(route), direction, :]]
times = pd.date_range(start=first_reading, end=last_reading, periods=len(stations))
plt.plot(times, stations.stop_name, linestyle='--')
for ti in lib.longest_trips(d, route, direction, n).index:
	lib.plot_trip(d, route, direction, ti)
