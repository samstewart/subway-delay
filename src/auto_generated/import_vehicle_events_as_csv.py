# convert the vehicle moved events to a csv files 
from schema import * 
import sys
import csv
import sqlalchemy
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
import gtfs_realtime_pb2 
import nyct_subway_pb2 
from os.path import splitext

fname = sys.argv[1]
output_fname = splitext(fname)[0] + '.csv'
 
print(fname + ' -> ' + output_fname)
def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

def vehicles_to_csv(fname, output_fname):
	statuses = ['incoming', 'stopped', 'in transit']	
	with open(output_fname, 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')

		events = load_feed_events(fname)
		header = ['trip_id', 'start_date', 'route_id', 'train_id', 'direction', 'current_stop_sequence', 'current_status', 'timestamp', 'stop_id', 'message_timestamp']
		writer.writerow(header)
		for event in events.entity:
			if event.HasField('vehicle'): 
				vehicle = event.vehicle
				trip = vehicle.trip
				trip_ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
				line = [trip.trip_id, trip.start_date, trip.route_id, trip_ext.train_id, trip_ext.direction, vehicle.current_stop_sequence, vehicle.current_status, vehicle.timestamp, vehicle.stop_id, events.header.timestamp]
				writer.writerow(line)	
				
vehicles_to_csv(fname, output_fname)
