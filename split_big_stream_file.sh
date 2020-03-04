#! /bin/bash

# each file started by 'n'
csplit -z $1 /^n$/ '{*}'

# then each of these files need to have a newline appended and the EOL trimmed off the end
# files are named as 'xx01', etc
for filename in xx*; do
	# trim EOL
	truncate -s -1 $filename
	# add newline
	sed -i '1s/^/\n/' $filename
done

