
# seems to have trouble with python 3
import gtfs_realtime_pb2 
import nyct_subway_pb2 
import sys
import sqlalchemy
import pandas as pd
import sqlalchemy
from sqlalchemy import text




database = sys.argv[1]
fname = sys.argv[2]

# todo: strip this after debugging. change to postgres default user?
connect_url = 'postgresql://{}:{}@{}:{}/{}'.format('sams', 's414j94s', 'localhost', 5432, database)
print(connect_url)
engine = sqlalchemy.create_engine(connect_url)

f = open(fname, "rb")
message = gtfs_realtime_pb2.FeedMessage()
message.ParseFromString(f.read())

message_timestamp = message.header.timestamp
entity = message.entity[0]
trip = entity.trip_update.trip
# start a transaction
with engine.begin() as connection:
	ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
	values = {'trip_id': trip.trip_id, 
		'observed_at': message_timestamp, 
		'start_date': trip.start_date, 
		'route_id': trip.route_id, 
		'train_description': ext.train_id, 
		'is_assigned': ext.is_assigned, 
		'direction': ext.direction}

	connection.execute(
	text("""
	INSERT INTO realtime_trips VALUES
	(
		:trip_id,
		:observed_at,
		:start_date,
		:route_id,
		:is_assigned,
		:direction,
		:train_description
	)
	ON CONFLICT (id)
	DO UPDATE SET observed_at = :observed_at
	"""),
	values)
	
	stop_time_update = entity.trip_update.stop_time_update[0]
	print(stop_time_update)

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
