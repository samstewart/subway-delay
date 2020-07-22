import pymongo
import os
from tqdm import tqdm
import numpy as np
import datetime
import pandas as pd

port = 27017
# todo: is there a way to keep the username and password out and use pycharm DB storage?
client = pymongo.MongoClient(f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PWD')}@localhost:{port}/gtfs?authSource=gtfs")
db = client.gtfs
route = db.routes.find_one()['stop_names']
db.trips.delete_many({})

# we we are doing a "left join" against the index of the stop in the route
query = {
    "direction": "NORTH",
    "route": "1",
}

# keep track of the progress
with tqdm(total=db.cleaned_gtfs.count_documents(query), desc="Trips") as p:
   for event in db.cleaned_gtfs.find(query):
        # add the stop index
        if event['stop_name'] in route:
            event['stop_index'] = route.index(event['stop_name'])
        else:
            event['stop_index'] = None

        db.cleaned_gtfs.update_one({'_id': event['_id']}, {"$set": {"stop_index": event['stop_index']}})

        p.update(1)


