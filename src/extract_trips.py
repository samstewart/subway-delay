import pymongo
import os
from tqdm import tqdm
import numpy as np
import datetime
import pandas as pd

port = 27017
# todo: is there a way to keep the username and password out and use pycharm DB storage?
#print(f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PWD')}@localhost:{port}/gtfs?authSource=gtfs")
client = pymongo.MongoClient(f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PWD')}@localhost:{port}/gtfs?authSource=gtfs")
#client = pymongo.MongoClient(f"mongodb://localhost:27017/gtfs")
db = client.gtfs
route = db.routes.find_one()['stop_names']
db.trips.delete_many({})
# has two separate trips we need to break apart
#"trip_id": "007200_1..N"
query = {
    "direction": "NORTH",
    "route": "1",
}
results = db.cleaned_gtfs.find(query) \
.sort([('train_id', pymongo.ASCENDING), ('trip_id', pymongo.ASCENDING), ('timestamp', pymongo.ASCENDING)])
# according to docs trip_id is unique up to (weekday, sat, sunday)
# only the trip ID and date *together* make a unique key.
event = results.next()


# keep track of the progress
with tqdm(total=db.cleaned_gtfs.count_documents(query), desc="Trips") as p:
    last_stop_time = event['timestamp']
    trip_start_date = last_stop_time
    cur_trip = [event]
    cur_trip_id = event['trip_id']
    cur_train_id = event['train_id']
    trips = []
    for event in results:
        # start of new trip
        hour = 60 * 60
        day = hour * 24
        diff = (event['timestamp'] - last_stop_time)
        if diff.days * day + diff.seconds > hour or cur_trip_id != event['trip_id'] or cur_train_id != event['train_id']:
            # important that we copy!
            db.trips.insert_one({"events": cur_trip.copy(),
                                 "trip_id": cur_trip_id,
                                 "train_id": cur_train_id,
                                 # import that it has no time information
                                 "start_date": trip_start_date.replace(hour=0, minute=0, second=0,microsecond=0),
                                 "start_time": trip_start_date,
                                 "route": "1",
                                 "direction": "NORTH"})
#            for e in cur_trip:
#                if e['stop_name'] in route:
#                    e['stop_index'] = route.index(e['stop_name'])
#                else:
#                    e['stop_index'] = -1

            cur_train_id = event['train_id']
            trip_start_date = event['timestamp']
            p.update(len(cur_trip))
            cur_trip_id = event['trip_id']
#            trips.append(cur_trip)
            cur_trip = []

        last_stop_time = event['timestamp']
        cur_trip.append(event)

db.trips.insert_one({"events": cur_trip,
 "trip_id": cur_trip_id,
 "train_id": cur_train_id,
 # import that it has no time information
 "start_date": trip_start_date.replace(hour=0, minute=0, second=0,microsecond=0),
 "start_time": trip_start_date,
 "route": "1",
 "direction": "NORTH"})

p.update(len(cur_trip))
#trips.append(cur_trip)

