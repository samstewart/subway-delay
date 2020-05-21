#!/usr/bin/env python
import sys
from google.protobuf.json_format import MessageToJson 
import gtfs_realtime_pb2, nyct_subway_pb2
import json
import pymongo


def main():
	client = pymongo.MongoClient(
	       "mongodb://localhost:27017/gtfs?retryWrites=true&w=majority")
	db = client.gtfs

	gtfs_realtime = gtfs_realtime_pb2.FeedMessage()

	with open(sys.argv[1],"rb") as f:
		gtfs_realtime.ParseFromString(f.read())
		message_as_json = json.loads(MessageToJson(gtfs_realtime))
       
		# add the header info to each event
		events = message_as_json['entity']
		for e in events:
			if 'vehicle' in e:
				e['header'] = message_as_json['header'].copy()
				db.events.insert(e)
 
if __name__ == '__main__':
	main()
