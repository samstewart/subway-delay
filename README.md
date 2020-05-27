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

# To Do
Focus on 1 Line
Estimate time between stops/trip time (‘at stop’ to ‘at stop’)
We want to determine expected travel time given the stations
Time of day, day of week, stop, etc.
Does written schedule trip time change depending on time of day?

[offset string](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
Tasks:
Sam: train line 1
Matt: train line 2
Sarah: train line 3
Compute average trip time for fixed station
Overall
Time of day
Day of the week (after we have more data)
Make plots of these to look for patterns
Sum up average of a few trips to see if it at all matches with trip time on schedule
Given average trip time for whole week’s worth of data, compute delay (difference between actual time and average time)
Plot deviance from average travel time
Look at travel times for 2 and 3 when they run to the same stops at 1. Are these times correlated?

Time between trains at a given stop (metric of delay: standard deviation from the mean)
Does the distribution of time between trains look poisson? (plot it!)
Does it vary by time of day? (mean frequency by hour)
Rush hour indicators (morning, afternoon/evening)
Possibly be able to recover where delays happen and watch them propagate. To find delays, look for when time between trains changes. If it’s usually 5 mins between trains, when does this pattern change?
Put time between stations code in repo
Figure out whether to use tripId or trainId
Ask Anne: why does Line 3 list stops as ‘stopped at’ that are not on its schedule? What’s tripId vs trainId?

-Plot median over time on histograms
-Ask Anne: If a train gets swapped out in the middle of a route, does “its” trainID or tripID change? When does trainID change?
-Make more histograms (by hour, day of week, stop)
-Find interesting stops: take median and standard deviation of time between trains over all time
-Input time between trains from schedule
-Model time between trains at a given stop, using time of day
    -Linear regression
    -Time series modeling (Cora Brown guest lecture)
    -Stationarize the data (differencing)
    -Recurrent neural network
    -LSTM (long short term memory)

Q: can we detect delays? 
can we see delay move along the route? does delay of one trip impact other trips on same route? what about
other routes?

summary of what I learned: we have an arrival process, Poisson process is special case with memoryless
distribution on interarrival times. Always three equivalent ways to specify arrival process:
total number of arrivals in interval (0, T)
interarrival times
first time when we've seen n arrivals
last two are units of time, first is number of arrivals.

Poisson defined via memoryless property of interarrival times?
Poisson process is stationary and has stationary increments? 

Model process for Poisson is sequence of bernoulli variables. In fact also only discrete arrival process
with geometric interarival distribution. 

Good to think about our problem as arrival process but it does not satisfy memoryless property

What are some easy necessary conditions of memoryless property to check?

network packing delivery is a good model
Queuing theory is the general frameowrk


