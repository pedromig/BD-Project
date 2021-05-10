#!/bin/bash

# Use the --no-start option to compose the images only
# Usage: ./compose.sh --no-start

# Use the -d option to compose the images and run
# containers from those images in the background
# Usage: ./compose.sh -d

mkdir -p ../src/app/logs
docker-compose -f compose.yml up --build "$@"
