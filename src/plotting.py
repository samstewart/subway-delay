def plot_longest_trips():
    reload(lib)
    d = lib.load_data('data/raw/realtime/stream.csv')

    # change these to plot different routes and directions
    route = "1"
    direction = 1
    n = 10

    first_reading = d.loc[idx[route, direction, :, :, :]].head(1).index.get_level_values('timestamp')[0]
    last_reading = d.loc[idx[route, direction, :, :, :]].tail(1).index.get_level_values('timestamp')[0]
    # can deduce this from the data
    # ideally route would a string key, but it is choosing integer instead
    # kind of inefficient to reload this everytime, should we pass it in?
    stations = \
    pd.read_csv('data/raw/static_transit/route_stops.csv', index_col=['route', 'direction', 'stop_index']).loc[
        idx[int(route), direction, :]]
    times = pd.date_range(start=first_reading, end=last_reading, periods=len(stations))
    plt.plot(times, stations.stop_name, linestyle='--')
    for ti in lib.longest_trips(d, route, direction, n).index:
        lib.plot_trip(d, route, direction, ti)

def plot_time_between_trains():
    d = lib.load_data('data/processed/team_data.csv')
    fourteenth_st = d.loc[idx["1", 'NORTH', :, '14 St', :], 'vehicle.currentStatus'].sort_index(
        level='vehicle.timestamp')
    fourteenth_st
    fourteenth_st = fourteenth_st[fourteenth_st == 'STOPPED_AT']
    times = pd.Series(fourteenth_st.index.get_level_values('vehicle.timestamp')).diff()
    diffs = times[times.notnull()] / pd.Timedelta(minutes=1)
    diffs.hist(bins=range(0, 20, 1))
