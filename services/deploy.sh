#!/bin/bash

# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Build everything
for i in `ls */dockerbuild.sh`; do sh $i; done

# Run everything
for i in `ls */dockerrun.sh`; do sh $i; done
