#!/usr/bin/env python
import pymongo
import time
import os
import sys
import datetime
from pprint import pprint
# take stuff from raw stream and make sure no duplicate entries / fix types
if __name__ == '__main__':
    # need tunnel from 27018 to 27017 on remote
    total = 0
    port = 27018
    client = pymongo.MongoClient(
        f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PWD')}@localhost:{port}/gtfs?authSource=gtfs&readPreference=primary&ssl=false")
    db = client.gtfs
    duplicates = 0
    #db.cleaned_gtfs.delete_many({})
    #sys.exit()
    #print(db.events.find({"vehicle": {"$exists": False}}).count())
    t0 = time.time()
    for event in db.events.find().limit(20):
        vehicle = event['vehicle']
        trip = vehicle['trip']
        stop_name = db.stops.find_one({"stop_id": vehicle['stopId']}, projection={'stop_name': True, '_id': False})
        if stop_name:
            stop_name = stop_name['stop_name']

        cleaned = {
            "direction": trip['[nyctTripDescriptor]']['direction'],
            "train_id": trip['[nyctTripDescriptor]']['trainId'],
            "status": vehicle["currentStatus"],
            'timestamp': datetime.datetime.fromtimestamp(int(vehicle['timestamp'].strip())),
            "stop_name": stop_name,
            "trip_id": vehicle['trip']['tripId'],
            "route": trip["routeId"]
        }
        try:
            db.cleaned_gtfs.insert_one(cleaned)
        except pymongo.errors.DuplicateKeyError:
            duplicates += 1

        if total % 10**5 == 0:
            print(f'Total processed {total}')
    t1 = time.time()
    print(f'Total time: {t1 - t0}')
    print(f'Duplicates: {duplicates}')
    #print(db.cleaned_gtfs.create_index([("timestamp", pymongo.DESCENDING), ("direction", pymongo.DESCENDING), ("trip_id", pymongo.DESCENDING)], unique=True))

