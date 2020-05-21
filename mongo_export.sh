#!/bin/bash

mongoexport --type=csv --out=test.csv --fieldFile=fields_from_database_for_csv.txt --db=gtfs --collection=csv_export
