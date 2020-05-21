subway-delay
==============================



Data
------------

The data from the realtime feed of Bluetooth sensors is in 'data/raw/realtime/stream.csv'. This data is a summary of the data in the GTFS (Google Transit Feed Specification) file that is downloaded every thirty seconds from the server. Not all the columns are useful. Here's what the columns mean

trip_id - a trip is a single train along a route. For example, the 1 line going from South Ferry to the Bronx
start_date - kinda pointless since we have the timestamp field
route_id - not sure what this is for / how different than route id.
train_id - I can't figure out the difference between this and the trip ID though it has the source and destination of the train in the name. From reading another blog post, these IDs can be unreliable since they swap trains out mid route if mechanical failure, etc.
direction - 1: north, 2: west, 3: south, 4: east 
current_stop_sequence - cannot figure out what this means 
current_status, 0: train is incoming, 1: train is stopped at the station, 2: train departed the previous station and is heading towards this station
timestamp - sensor reading timestamp (in unix timestamp; see source for converting to pandas datetime)
stop_id - unique code that is used to look up the full stop name in the data/raw/static_transit/stops.txt list of stops. This is done for you if you use src/vehicle_trajectory (see the source code section)
message_timestamp - time we downloaded the message (in unix timestamp). this will thus be spaced thirty seconds apart

When you use the `load_data()` method in `src/vehicle_trajectory` it will automatically join the stop meta data (name, geoloc).

Loading the Data
------------------
The python module `src/vehicle_trajectory.py` has useful methods for parsing the data. See the docs in the file for more info. As an example, look at `src/plot_all_longest_trips.py`

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
