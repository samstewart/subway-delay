
from schema import * 
import sys

import sqlalchemy
from sqlalchemy import exists
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
RealtimePredictedArrival.__table__.create(engine, checkfirst=True)
Alert.__table__.create(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
s = Session()

def realtime_predicted_arrival_from_feed(trip, stop_time_update):
	# get the properties added by nyc
	ext = stop_time_update.Extensions[nyct_subway_pb2.nyct_stop_time_update]
	stop_id = stop_time_update.stop_id
	rp = RealtimePredictedArrival(realtime_trip_id = trip.trip_id,\
		actual_track = ext.actual_track,\
		scheduled_track = ext.scheduled_track)
	
	# sometimes the stops don't exist
	if s.query(exists().where(Stop.id==stop_id)).scalar():
		rp.stop_id = stop_id

	if stop_time_update.HasField('departure'):
		rp.departure_time = stop_time_update.departure.time
	if stop_time_update.HasField('arrival'):
		rp.arrival_time = stop_time_update.arrival.time
	
	return rp


def realtime_predicted_arrivals_from_feed(entity):
	trip = entity.trip
	
	return map(lambda u: realtime_predicted_arrival_from_feed(trip, u), entity.stop_time_update)

def realtime_trip_from_feed(trip):
	# get the properties added by nyc
	ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
	return RealtimeTrip(id = trip.trip_id,\
		start_date = trip.start_date,\
		route_id = trip.route_id,\
		direction = ext.direction,\
		is_assigned = ext.is_assigned,\
		train_description = ext.train_id)


def alert_from_feed(feed_alert, timestamp, messages):
		
	trip = create_or_update_realtime_trip(feed_alert.trip, timestamp)

	alert = Alert(message = messages, observed_at = timestamp)
	
	if feed_alert.HasField('trip'):
		alert.realtime_trip_id = feed_alert.trip.trip_id
	elif feed_alert.HasField('stop_id'):
		alert.stop_id = feed_alert.stop_id
	elif feed_alert.HasField('route_id'):
		alert.route_id = feed_alert.route_id
	
	return alert

def alerts_from_feed(event, timestamp):
	messages = ','.join([("%d - %s" % (i, t.text)) for (i, t) in enumerate(event.alert.header_text.translation)])
	
	return map(lambda a: alert_from_feed(a, timestamp, messages), event.alert.informed_entity) 


def vehicle_moved_from_feed(entity, message_timestamp):
	vehicle = entity.vehicle
	trip = vehicle.trip 
	r = RealtimeTrainMoved(realtime_trip_id = trip.trip_id,\
		last_moved_time = vehicle.timestamp,\
		message_timestamp = message_timestamp,\
		current_stop_sequence = vehicle.current_stop_sequence,\
		current_status = vehicle.current_status)

	stop_id = vehicle.stop_id

	if s.query(exists().where(Stop.id==stop_id)).scalar():
		r.stop_id = stop_id
	
	return r

def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

def create_or_update_realtime_trip(trip, timestamp):
	# add or update the trip		
	stored_trip = s.query(RealtimeTrip).filter_by(id=trip.trip_id).first()

	if stored_trip:	
		stored_trip.observed_at = timestamp 
	else:
		stored_trip = realtime_trip_from_feed(trip)
		stored_trip.observed_at = timestamp
		s.add(stored_trip)

	return stored_trip
	

def import_feed_events(fname, s):

	events = load_feed_events(fname)
	for event in events.entity:
		if event.HasField('vehicle'):
			trip = create_or_update_realtime_trip(event.vehicle.trip, events.header.timestamp)
	
			moved = vehicle_moved_from_feed(event, events.header.timestamp)
			s.add(moved)

		elif event.HasField('alert'):
			for alert in alerts_from_feed(event, events.header.timestamp):
				# add or update the trip		
				s.add(alert)
		elif event.HasField('trip_update'):
			trip = create_or_update_realtime_trip(event.trip_update.trip, events.header.timestamp)

			for u in realtime_predicted_arrivals_from_feed(event.trip_update):
				s.add(u)

			
	s.commit()

	s.close()

import_feed_events(fname, s)
