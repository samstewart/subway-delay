
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
#if we want to create the table 
Alert.__table__.create(engine,checkfirst=True)

Session = sessionmaker(bind=engine)
s = Session()

def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

events = load_feed_events(fname)
for event in events.entity:
	if event.HasField('alert'):
#		print(event.alert.informed_entity)
		for alert in alerts_from_feed(event, events.header.timestamp):
			# add or update the trip		
			s.add(alert)

s.commit()

s.close()

