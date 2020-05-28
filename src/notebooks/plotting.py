
import pymongo
import pandas as pd
import numpy as np

def median_interval_weekday(dates):
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    resampled = dates.between_time('7:00', '18:00')
    #resampled = resampled[resampled.index.weekday <= 4]
    #resampled = resampled.resample('B').median()
    return resampled.groupby(resampled.index.weekday_name).median().reindex(days)

def get_train_trajectory(db, start, end, trip_id):
    results = db.cleaned_gtfs.find({
        "trip_id": trip_id,
        "timestamp": {"$lt": end, "$gte": start},
    },
        projection={"timestamp": True, "stop_name": True, "trip_id": True, "status": True, "_id": False}) \
        .sort([('timestamp', pymongo.ASCENDING)])

    return pd.DataFrame(list(results)).set_index('timestamp')

def get_trips_stop_at_time(db, stop_time, stop_name, direction, route):
    results = db.cleaned_gtfs.find({
        "stop_name": stop_name,
        "direction": direction,
        "route": route,
        "status": "STOPPED_AT",
        "timestamp": stop_time
    },
          projection={"trip_id": True,
                    "_id": False})
    return pd.DataFrame(list(results))

def get_stops(db, start, end, direction, route):
    results = db.cleaned_gtfs.find({
        "direction": direction,
        "route": route,
        "timestamp": {"$lt": end, "$gte": start}
    },
          projection={"timestamp": True,
                    "trip_id": True,
                    "_id": False}) \
        .sort([('timestamp', pymongo.ASCENDING)])
    return pd.DataFrame(list(results)).set_index('timestamp')

def all_stop_times(db, start, end, stop_names):
    results = db.cleaned_gtfs.find({
       "stop_name": {"$in": stop_names},
       "direction": "NORTH",
       "route": "1",
       "status": "STOPPED_AT",
       "timestamp": {"$lt": end, "$gte": start},
    },
    projection={"timestamp": True, "stop_name":True, "_id": False})\
    .sort([('stop_name', pymongo.ASCENDING), ('timestamp', pymongo.ASCENDING)])

    results = pd.DataFrame(list(results))
    # now make the stop names the columns so that we have a column for each set of timeseries data.
    # requires some annoying index twiddling.

    # here we make a counter for the rows. the pivot command is kind of irritating since the index needs to index the
    # rows of the pivoted table
    counts = results.groupby('stop_name').count()
    results.index = np.hstack([np.arange(n) for n in counts['timestamp']])
    return results.pivot(columns='stop_name', values='timestamp').reindex(stop_names, axis='columns')


