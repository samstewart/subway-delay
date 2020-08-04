pd.DataFrame(list(db.cleaned_gtfs.aggregate([
    {"$match": {"direction": 'NORTH', "route": '1'}},
    # create new day of week field
    {"$addFields": {
        # add day of week field
        "weekday": {"$dayOfWeek": "$timestamp"}}
    },
    # get only weekdays
    {"$match": {"weekday": {"$lte": 6, "$gte": 2}}},
    # breakup the train id into pieces
    # todo: the fact that split does not eat all the spaces leaves
    # an element in the train_info array that is '' (for some of them).
    {"$addFields":  # break the train info into pieces
        {"train_info_pieces": {
            "$filter": {
                "input": {"$split": ["$train_id", " "]},
                "as": "info",
                # what do double dollar signs mean? reference temporary variable. See 'let' expression.
                # get rid of the '' empty elements from the split
                "cond": {"$not": {"$eq": ["$$info", '']}}
            }
        }
        }},
    {"$addFields": {
        "train_info.type": {"$arrayElemAt": ["$train_info_pieces", 0]},
        "train_info.start":
            {"$trim": {
                "input": {"$arrayElemAt": ["$train_info_pieces", 1]},
                "chars": "+"}},
        "train_info.desc": {"$arrayElemAt": ["$train_info_pieces", 2]}
    }},
    {"$addFields": {
        "train_info.start.hour":
            {"$toInt":
                 {"$substr": ["$train_info.start", 0, 2]}
             },
        "train_info.start.minute":
            {"$toInt":
                 {"$substr": ["$train_info.start", 2, -1]}
             }
    }},
    {"$addFields": {
        "train_info.start.total_milliseconds": {"$add": [
            # convert both to milliseconds
            {"$multiply": ["$train_info.start.hour", 60, 60, 1000]},
            {"$multiply": ["$train_info.start.minute", 60, 1000]}
        ]}
    }
    },
    # now truncate the timestamp to just the day (no time info)
    {"$addFields":
        {"day":
            {"$dateFromString":
                {"dateString":
                    {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}
                    }
                }
            }
        }
    },
    # now finally we add the origin time (won't work for things close to 23h)
    {"$addFields": {"origin_timestamp": {"$add": ["$day", "$train_info.start.total_milliseconds"]}}},
    # fix the timestamp field by bumping forward one hour (don't know why origin_timestamp and the timestamps are off by an hour?)
    {"$addFields": {"timestamp": {"$add": ["$timestamp", 3600000]}}},
    {"$out": "weekdays"}
    #    {"$match": {"train_desc": None}},

    #    {"$limit": 10}
])))