.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################
# mapping from name of train line to ID for feed url request
#  MAPPING = {
#    "1" => 1,
#    "2" => 1,
#    "3" => 1,
#    "4" => 1,
#    "5" => 1,
#    "5X" => 1,
#    "6" => 1,
#    "6X" => 1,
#    "7" => 51,
#    "GS" => 1,
#    "A" => 26,
#    "B" => 21,
#    "C" => 26,
#    "D" => 21,
#    "E" => 26,
#    "F" => 21,
#    "G" => 31,
#    "J" => 36,
#    "L" => 2,
#    "M" => 21,
#    "N" => 16,
#    "Q" => 16,
#    "R" => 16,
#    "W" => 16,
#    "Z" => 36,
#    "SI" => 11
#  }


#################################################################################
# where to find data

# the static data
STATIC_DATA_FILES = calendar_dates.txt calendar.txt routes.txt shapes.txt stops.txt stop_times.txt transfers.txt trips.txt

# I have no idea how they generated these. there is not a 1-1 match between train lines either
FEED_IDS = 1 21 51 26 36 2 16 11
REALTIME_TABLES = alerts realtime_vehicle_moved realtime_trips realtime_predicted_arrivals 

export PYTHONPATH = src/auto_generated

STATIC_GTFS_DATA=http://web.mta.info/developers/data/nyct/subway/google_transit.zip
# query url to get realtime data in protocol buffer
# make sure to set the MTA_KEY as an environment variable!
# just for debugging
MTA_KEY=4354e649c64e51e6181051af63519238
GTFS_URL=http://datamine.mta.info/mta_esi.php?key=$(MTA_KEY)&feed_id=
DATABASE=subway

#################################################################################
# unix timestamp
CUR_TIME = $(shell date +%s)
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = subway-delay
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################
# create the database
database:
	# assumes that it doesn't already exist
	createdb $(DATABASE)

	
# todo: separate table creation into own command from import_events.py
delete_realtime_tables: $(addprefix delete_table/,$(REALTIME_TABLES))

delete_table/%:
	psql $(DATABASE) -c "drop table if exists $* cascade"


import_feeds: $(addprefix import_feed/,$(FEED_IDS))

# note: deletes files generated as prerequesites which is what we want
import_feed/%: data/raw/realtime/%.gtfs
	cp data/raw/realtime/$*.gtfs data/raw/realtime/$*_$(CUR_TIME).gtfs

# todo: should depend on downloaded. my dream is to bundle stuff into zip files
# pass the number of the data feed

# most elegant solution is to stream directly from download to one file (but then stopping gracefully is hard)
# xargs is functional currying
data/%_combined.gtfs:
	cat data/raw/realtime/$*_*.gtfs > data/$*_combined.gtfs

data/%_combined.csv: data/%_combined.gtfs
	python3 src/auto_generated/import_vehicle_events_as_csv.py data/$*_combined.gtfs
	
	

# one way to loop through all the gtfs files. for the moment I think it's easier just to use 'find'
#import_feeds_to_database: $(addprefix data/processed/,$(notdir $(wildcard data/raw/realtime/*.gtfs)))
			
## note debugging use -B
# download the realtime feed and import it into the database
data/raw/realtime/%.gtfs: 	
	# need to quote the url!
	wget --content-disposition -O $@ "$(GTFS_URL)$*"
	

# insert each of the files into the database and copy the schema to the data folder (let's Make track this target as built)
# preq:  data/raw/static_transit/%.txt (temporarily disable for debugging)
data/raw/static_transit/%.sql:
	cp src/data/static_schemas/$*.sql data/raw/static_transit
	# create the table by using the file copied above
	psql $(DATABASE) -f $@
	# output the command we'll use to insert into the database
	psql $(DATABASE) -c "\copy $* FROM 'data/raw/static_transit/$*.txt' (FORMAT CSV, DELIMITER(','), HEADER);" 

data/raw/static_transit/%.txt: # you ask for any of the data files, triggers whole download
	curl -o data/raw/static_transit.zip $(STATIC_GTFS_DATA)
	unzip -d data/raw/static_transit data/raw/static_transit.zip 
	# touch files so when we call make clean it doens't delete them
	find data/raw/static_transit -type f -exec touch {} +		
	rm data/raw/static_transit.zip

realtime_data: $(FEED_IDS)
	# todo: download 1.gtfs and insert all the records into the database

	
extract_static_data: download_data
	

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

delete_realtime_data:
	rm data/raw/realtime/*.gtfs

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
