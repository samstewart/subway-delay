#! /bin/bash
FEED_ID=1
MTA_KEY="4354e649c64e51e6181051af63519238"
GTFS_URL="http://datamine.mta.info/mta_esi.php?key=$MTA_KEY&feed_id=$FEED_ID"
#echo $MTA_KEY
#echo $GTFS_URL
#wget --quiet --content-disposition -O - "$GTFS_URL" 
while true; do
	echo "downloading"
	wget --quiet --content-disposition -O - "$GTFS_URL" >> data/raw/realtime/stream.gtfs 
	echo "done"
	sleep 30
done
