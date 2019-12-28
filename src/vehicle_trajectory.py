
import pandas as pd
from matplotlib import pyplot
import itertools
#trip_id,start_date,route_id,train_id,direction,current_stop_sequence,current_status,timestamp,stop_id,message_timestamp
# 096700_1..N03R,20191120,1,01 1607  SFT/242,1,38,1,1574287365,101N,1574287432
096700_1..N03R,20191120,1,01 1607  SFT/242,1,38,1,1574287365,101N,1574287432

f = pd.read_csv('test.csv')

# get a trip with at least 68 updates (that is the most number of updates we've seen)
number_of_times = f[f.route_id == "1"].groupby('trip_id').size()
trip_id = number_of_times.index[number_of_times >= 68][0]
# the status codes
#statuses = ['incoming', 'stopped', 'in transit']	
f[f.trip_id == trip_id].groupby(['stop_id', 'current_status']).size().head(10)
one_trip = f[f.trip_id == trip_id].copy()
one_trip.timestamp = pd.to_numeric(one_trip.timestamp)
one_trip.message_timestamp = pd.to_numeric(one_trip.message_timestamp)
short_snapshot = one_trip[['stop_id', 'current_status', 'timestamp', 'message_timestamp']].sort_values(by=["stop_id", "timestamp"], ascending=[False, True]).head(10)
short_snapshot
short_snapshot['t_delta'] = (short_snapshot['timestamp'] - short_snapshot['timestamp'].shift()).fillna(0)
# so in transit means we left the previous stop (so we departed last stop)
# incoming means we are arriving at the current station

short_snapshot.index
# problem is that we need to reindex when subsetting. or maybe I should be choosing a smarter index?
start
start = short_snapshot.at[4705,'timestamp']
# if I double my sample frequency will I see the proper sequence 0,1,2?
short_snapshot['timestamp'] = pd.to_datetime(pd.to_numeric(short_snapshot['timestamp']), unit='s')

short_snapshot['message_timestamp'] = pd.to_datetime(pd.to_numeric(short_snapshot['message_timestamp']), unit='s')

short_snapshot
one_trip[one_trip.stop_id.isin(["103N", "104N", "106N"])][['current_status', 'timestamp', 'message_timestamp']]
one_trip[one_trip.stop_id == "104N"][['current_status', 'timestamp', 'message_timestamp']]
one_trip[one_trip.stop_id == "106N"][['current_status', 'timestamp', 'message_timestamp']]
one_trip[one_trip.stop_id == "107N"][['current_status', 'timestamp', 'message_timestamp']]
# todo: convert columns to the correct datatypes?
f[f.trip_id == trip_id].groupby('stop_id').size().sort_index(axis=0, ascending=False)

# multiple trains for one trip? no
f[f.trip_id == trip_id].groupby('train_id').size()
