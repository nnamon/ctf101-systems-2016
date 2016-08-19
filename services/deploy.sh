#!/bin/bash

# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Build and run everything
for i in `ls -d */`; do
    cd $i
    ./dockerbuild.sh
    ./dockerrun.sh
    cd ..
done

