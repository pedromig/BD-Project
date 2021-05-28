#!/bin/bash

# Just a simple script to help in the development fase of this project
# Removes all the containers images and folders created by the compose script

API="auction-rest-api"
DB="db"

docker rm "${API}" "${DB}" -v
docker rmi "${API}:latest" "${DB}:latest" -f
docker image prune -f
rm -rf ../src/app/logs
