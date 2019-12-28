# count the different kinds of events in a gtfs file. for my own curiosity
from schema import * 
import sys

import sqlalchemy
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
import gtfs_realtime_pb2 
import nyct_subway_pb2 

fname = sys.argv[1]

def load_feed_events(fname):
	with open(fname, "rb") as f:
		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(f.read())

		return message

def count_feed_events(fname):
	counts = {'vehicle': 0, 'alert': 0, 'trip_update': 0}
	events = load_feed_events(fname)
	for event in events.entity:
		for k, v in counts.items():
			if event.HasField(k):
				counts[k] = counts[k] + 1	
	return counts

print(count_feed_events(fname))
