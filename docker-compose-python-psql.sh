
#docker rm $(docker stop $(docker ps -a -q)) 

mkdir -p python/app/logs

# add  -d  to the command below if you want the containers running in background without logs
docker-compose  -f docker-compose-python-psql.yml up --build
