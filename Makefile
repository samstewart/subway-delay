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

STATIC_GTFS_DATA=http://web.mta.info/developers/data/nyct/subway/google_transit.zip
# query url to get realtime data in protocol buffer
# make sure to set the MTA_KEY as an environment variable!
GTFS_URL=http://datamine.mta.info/mta_esi.php?key=$(MTA_KEY)&feed_id=
DATABASE=subway

#################################################################################

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

## note debugging use -B

# insert the downloaded static data into f

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

#.PHONY: data/raw/realtime/%.gtfs
data/raw/realtime/%.gtfs: 	
	# the '$*' expands just the matched part for % (in this case a number)
	# need to quote the url!
	wget --content-disposition -O $@ "$(GTFS_URL)$*"
		
extract_static_data: download_data
	

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
