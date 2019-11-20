#!/bin/bash
# meant to be run from root of project

PREFIX=src/auto_generated
# add relative to root of project
export PYTHONPATH=$PYTHONPATH:src/auto_generated
# ordering is important here!
python3 $PREFIX/import_stop_time_updates.py $1 $2
python3 $PREFIX/import_vehicle_positions.py $1 $2
python3 $PREFIX/import_alerts.py $1 $2
