
from schema import RealtimeTrip, RealtimeTrainMoved, Alert
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
RealtimeTrainMoved.__table__.create(engine, checkfirst=True)
Alert.__table__.create(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
s = Session()

def realtime_trip_from_feed(entity):
	trip = entity.trip_update.trip
	# get the properties added by nyc
	ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
	return RealtimeTrip(id = trip.trip_id,\
		start_date = trip.start_date,\
		route_id = trip.route_id,\
		direction = ext.direction,\
		is_assigned = ext.is_assigned,\
		train_description = ext.train_id)


def alerts_from_feed(entity, timestamp):
	messages = ','.join([("%d - %s" % (i, t.text)) for (i, t) in enumerate(event.alert.header_text.translation)])
	alerts = []
	for informed in entity.alert.informed_entity:
		alert = Alert(message = messages, observed_at = timestamp)
		
		if informed.HasField('trip'):
			alert.realtime_trip_id = informed.trip.trip_id
		elif informed.HasField('stop_id'):
			alert.stop_id = informed.stop_id
		elif informed.HasField('route_id'):
			alert.route_id = informed.route_id

		alerts.append( alert)

	return alerts


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

def create_or_update_realtime_trip(event):
	# add or update the trip		
	trip = s.query(RealtimeTrip).filter_by(id=event.trip.trip_id).first()

	if trip:	
		trip.observed_at = timestamp 
	else:
		trip = realtime_trip_from_feed(event)
		trip.observed_at = timestamp
		s.add(trip)

	return trip	
	

def import_feed_events(fname, s):

	events = load_feed_events(fname)
	for event in events.entity:
		if event.HasField('vehicle'):
			break
			trip = create_or_update_realtime_trip(event)
			moved = vehicle_moved_from_feed(event)
			moved.trip = trip
			# is this step necessary
			moved.realtime_trip_id = trip.id
			s.add(moved)

		elif event.HasField('alert'):
			break
			for alert in alerts_from_feed(event, events.header.timestamp):
				# add or update the trip		
				s.add(alert)
		elif event.HasField('trip_update'):
			print(event)
			# todo: create realtime_predicted_arrivals object
			break
			trip = create_or_update_realtime_trip(event)
			
	s.commit()

	s.close()

import_feed_events(fname, s)
