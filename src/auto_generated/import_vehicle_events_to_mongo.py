#!/usr/bin/env python
import sys
from google.protobuf.json_format import MessageToJson
import auto_generated.gtfs_realtime_pb2,auto_generated.nyct_subway_pb2
import json
import pymongo
import requests

def main():
#	client = pymongo.MongoClient(
#	       "mongodb://localhost:27017/gtfs?retryWrites=true&w=majority")
#	db = client.gtfs
	r = requests.get(f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
				 headers={"x-api-key": "kDjAqBL0oj2xaVN9F4AdM4fFwgsSYfRY7D6BjYtx"})
	gtfs_realtime = auto_generated.gtfs_realtime_pb2.FeedMessage()

	gtfs_realtime.ParseFromString(r.content)
	message_as_json = json.loads(MessageToJson(gtfs_realtime))
	print(json.dumps(message_as_json, indent=1)	)

		# add the header info to each event
#		events = message_as_json['entity']
#		for e in events:
#			if 'vehicle' in e:
#				e['header'] = message_as_json['header'].copy()
#				db.events.insert(e)
 
if __name__ == '__main__':
	main()
