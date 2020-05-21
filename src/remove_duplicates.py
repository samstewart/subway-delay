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

if __name__ == '__main__':
	main()
