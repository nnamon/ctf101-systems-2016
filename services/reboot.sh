#!/bin/bash

# Stop all containers
docker stop $(docker ps -a -q)

# Run everything
for i in `ls -d */`; do
    cd $i
    ./dockerrun.sh
    cd ..
done

