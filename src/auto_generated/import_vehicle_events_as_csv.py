# convert the vehicle moved events to a csv files 
import sys
import csv
import gtfs_realtime_pb2 
import nyct_subway_pb2 
from os.path import splitext

fname = sys.argv[1]
output_fname = splitext(fname)[0] + '.csv'
 
def load_feed_events(fname):
    with open(fname, "rb") as f:
        message = gtfs_realtime_pb2.FeedMessage()
        message.MergeFromString(f.read())

        return message

def vehicles_to_csv(fname, output_fname):
    statuses = ['incoming', 'stopped', 'in transit']
    csvfile = open(output_fname, 'w')
    writer = csv.writer(csvfile, delimiter=',')
        
    events = load_feed_events(fname)
    header = ['trip_id', 'start_date', 'route_id', 'train_id', 'direction', 'current_stop_sequence', 'current_status', 'timestamp', 'stop_id', 'message_timestamp']
    writer.writerow(header)
    print('wrote header')
    rows_before_flush = 1000
    row = 0
    for event in events.entity:
            if event.HasField('vehicle'): 
                    row += 1
                    vehicle = event.vehicle
                    trip = vehicle.trip
                    trip_ext = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
                    line = [trip.trip_id, trip.start_date, trip.route_id, trip_ext.train_id, trip_ext.direction, vehicle.current_stop_sequence, vehicle.current_status, vehicle.timestamp, vehicle.stop_id, events.header.timestamp]
                    writer.writerow(line)
                    if row > rows_before_flush:
                            print('flushed')
                            csvfile.flush()
                            row = 0
                    
vehicles_to_csv(fname, output_fname)
