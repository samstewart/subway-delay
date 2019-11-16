
# seems to have trouble with python 3
import gtfs_realtime_pb2 
import json
import nyct_subway_pb2 
import sys
import sqlalchemy
import pandas as pd
import sqlalchemy
from sqlalchemy import text, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


database = sys.argv[1]
fname = sys.argv[2]

class Route(Base):
	__tablename__ = 'routes'
	id = Column(String(5), primary_key=True)
	agency_id = Column(String)
	route_short_name = Column(String)
	route_long_name = Column(String)
	route_desc = Column(String)
	route_type = Column(Integer)
	route_url = Column(Integer)
	route_color = Column(String)
	route_text_color = Column(String)
	realtime_trips = relationship('RealtimeTrip')

# the realtimet trip
class RealtimeTrip(Base):
	__tablename__ = 'realtime_trips'
	id = Column(String(30), primary_key=True)
	observed_at = Column(Integer)
	start_date = Column(String(10))
	route_id = Column(String(5),ForeignKey('routes.id'))
	direction = Column(String(10))
	is_assigned = Column(Boolean)
	train_description = Column(String(30))
	route = relationship('Route', back_populates='realtime_trips')
	
	def __repr__(self):
		return  'RealtimeTrip(%s, %s)' % (self.id, self.route_id)
	
# todo: strip this after debugging. change to postgres default user?
connect_url = 'postgresql://{}:{}@{}:{}/{}'.format('sams', 's414j94s', 'localhost', 5432, database)
engine = sqlalchemy.create_engine(connect_url)
#print(RealtimeTrip.__table__.create(engine))
Session = sessionmaker(bind=engine)
s = Session()
#trip = RealtimeTrip(id = 'HI', observed_at = 1, start_date = '1', route_id = '1', direction = 'SOUTH', is_assigned = False, train_description = 'you')
#s.add(trip)

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
s.add(realtime_trip_from_feed(events.entity[0], events.header.timestamp))
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
