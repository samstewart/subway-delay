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
d = lib.load_data('data/processed/team_data.csv')
fourteenth_st = d.loc[idx["1", 'NORTH', :, '14 St', :], 'vehicle.currentStatus'].sort_index(level='vehicle.timestamp')
fourteenth_st
fourteenth_st = fourteenth_st[fourteenth_st == 'STOPPED_AT']
times = pd.Series(fourteenth_st.index.get_level_values('vehicle.timestamp')).diff()
diffs = times[times.notnull()] / pd.Timedelta(minutes=1)
diffs.hist(bins=range(0, 20, 1))

fourteenth_st.delta = (fourteenth_st.index['vehicle.timestamp'] - fourteenth_st.shift())

lib.plot_all_longest_trips(f, "1", 1, 10) 
