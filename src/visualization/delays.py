
import pandas as pd
from matplotlib import pyplot
import itertools
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:samuel@localhost/nyc_gtfs_development')

def hi():
	# test
	return 'hi'


def plot_trip(realtime_trip_id):
	query = "select * from time_between_stations where route_mta_id = 'L' and realtime_trip_id = %d order by origin_departure" % (realtime_trip_id, )
	trip = pd.read_sql(query, con=engine)
	pyplot.plot(trip['transit_time'].cumsum())
plot_trip(849)


# get the list of full length
query = "select * from full_length_L_trips";
ids = pd.read_sql(query, con=engine)['id'].tolist()

# it appears that the trip with id 1230 has a big delay in the middle
ids[-4]
realtime_trip_id = ids[-4]
trip['transit_time'][10]
# goddamn it, the time stamps are in NY time while the vehicle positions are in UTC
trip.loc[10, ['realtime_trip_id', 'origin_departure', 'dest_arrival']]
trip.loc[10 ]
trip[trip['transit_time'] < 40]
type(l)
trip[7:13]

realtime_trip_id
realtime_trip_id = ids[2]

pyplot.cla()
offset = 0
for realtime_trip_id in ids:
query = "select * from time_between_stations where route_mta_id = 'L' and realtime_trip_id = %d order by origin_departure" % (realtime_trip_id, )
trip = pd.read_sql(query, con=engine)
pyplot.plot(trip['transit_time'].cumsum() + offset)
offset += 250 
