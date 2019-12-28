# count the different kinds of events in a gtfs file. for my own curiosity
from schema import * 
import sys

import sqlalchemy
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
import gtfs_realtime_pb2 
import nyct_subway_pb2 

fname = sys.argv[1]
#print(fname)
def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

def inspect_vehicle(fname):
	statuses = ['incoming', 'stopped', 'in transit']	
	#counts = [0,0,0]
	events = load_feed_events(fname)
	for event in events.entity:
		if event.HasField('vehicle') and event.vehicle.trip.route_id == "1":
#			print(event.vehicle)
			train1_id = "087150_1..S03R"
			trainL_id = "084050_L..S"
			if event.vehicle.trip.trip_id == train1_id: 
#				print(event.vehicle.current_stop_sequence)			
				print(event.vehicle.stop_id)
#				print(statuses[event.vehicle.current_status])
	#		counts[event.vehicle.current_status] += 1

inspect_vehicle(fname)
