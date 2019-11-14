
import gtfs_realtime_pb2 
import nyct_subway_pb2 
import sys

f = open(sys.argv[1], "rb")

message = gtfs_realtime_pb2.FeedMessage()

message.ParseFromString(f.read())

#print message.header.timestamp
#event = message.entity[2]

for event in message.entity:
	if event.HasField('alert'):
		print event

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
f.close()
