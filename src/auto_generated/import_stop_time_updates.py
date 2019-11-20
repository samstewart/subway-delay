
# seems to have trouble with python 3
from schema import RealtimeTrip
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

RealtimeTrip.__table__.create(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
s = Session()

def realtime_trip_from_feed(entity, message_timestamp):
	trip = entity.trip_update.trip
	# get the properties added by nyc
	ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
	return RealtimeTrip(id = trip.trip_id,\
		observed_at = message_timestamp,\
		start_date = trip.start_date,\
		route_id = trip.route_id,\
		direction = ext.direction,\
		is_assigned = ext.is_assigned,\
		train_description = ext.train_id)

def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

events = load_feed_events(fname)
for event in events.entity:
	if event.HasField('trip_update'):
		# add or update the trip		
		feed_trip = realtime_trip_from_feed(event, events.header.timestamp)
#		# do we already have such a trip then updated its observed time
		trip = s.query(RealtimeTrip).filter_by(id=feed_trip.id).first()
		if trip:	
			trip.observed_at = events.header.timestamp
		else:
			
			s.add(feed_trip)

s.commit()
## start a transaction
#with engine.begin() as connection:

#	connection.execute(
#	text("""
#	INSERT INTO realtime_trips VALUES
#	(
#		:trip_id,
#		:observed_at,
#		:start_date,
#		:route_id,
#		:is_assigned,
#		:direction,
#		:train_description
#	)
#	ON CONFLICT (id)
#	DO UPDATE SET observed_at = :observed_at
#	"""),
#	values)
#	
#	stop_time_update = entity.trip_update.stop_time_update[0]
#	print(stop_time_update)

#print message.header.timestamp
#event = message.entity[2]

#for event in message.entity:
#	if event.HasField('trip_update'):
#		print event

#print event
#if event.HasField('trip_update'):
##	print event.trip_update
##	How we use extensions
#	event.trip_update
##	print event.trip_update.trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
##	print event.trip_update.trip.nyct_trip_descriptor
#elif event.HasField('vehicle'):
#	
#	event.vehicle
#elif event.HasField('alert'):
#	event.alert
#
#  optional TripUpdate trip_update = 3;
#  optional VehiclePosition vehicle = 4;
#  optional Alert alert = 5;


#print(message.entity[0])
#f.close()
