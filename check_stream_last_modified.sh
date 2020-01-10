#! /bin/bash

# just see when the stream file was last modified. should be at most a minute ago if we are querying every 30 seconds
ssh linode "ls -l projects/subway-delay/data/raw/realtime/stream.gtfs" | awk '{print $8}'
