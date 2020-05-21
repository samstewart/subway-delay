#!/bin/bash

for f in data/raw/realtime/xx*; do
	echo $f
	python3 src/auto_generated/import_vehicle_events_to_mongo.py $f
done
