
from schema import RealtimeTrip, RealtimeTrainMoved
import sys

import sqlalchemy
from sqlalchemy.orm import sessionmaker
import gtfs_realtime_pb2 
import nyct_subway_pb2 

database = sys.argv[1]
fname = sys.argv[2]

# todo: strip this after debugging. change to postgres default user?
connect_url = 'postgresql://{}:{}@{}:{}/{}'.format('sams', 's414j94s', 'localhost', 5432, database)
engine = sqlalchemy.create_engine(connect_url)
#if we want to create the table 
#RealtimeTrainMoved.__table__.create(engine)

Session = sessionmaker(bind=engine)
s = Session()

def vehicle_moved_from_feed(entity):
	vehicle = entity.vehicle
	trip = vehicle.trip 
	return RealtimeTrainMoved(realtime_trip_id = trip.trip_id,\
		stop_id = vehicle.stop_id,\
		last_moved_time = vehicle.timestamp,\
		current_stop_sequence = vehicle.current_stop_sequence,\
		current_status = vehicle.current_status)

def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

events = load_feed_events(fname)
for event in events.entity:
	if event.HasField('vehicle'):
#		# add or update the trip		
		
		vehicle_moved = vehicle_moved_from_feed(event)
		s.add(vehicle_moved)

s.commit()

s.close()

