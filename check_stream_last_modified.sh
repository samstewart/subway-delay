#! /bin/bash

# just see when the stream file was last modified. should be at most a minute ago if we are querying every 30 seconds
# plots [size] [time modified]
# the -h flag gives human readable sizes
ssh linode "ls -lh projects/subway-delay/data/raw/realtime/stream.gtfs" | awk '{print $5, $8}'
