##### building and the Dockerfile itself

```bash
docker build --target dev . -t flasker
docker run -it -v ${PWD}:/work -p 5000:5000 --net redis flasker sh
```

##### redis clustering

- making use of redis sentinel for high availability

###### how to setup

- ensure you are using the same network across to do this 
```bash
docker network create redis
```

- you will need redis:7.4.2-alpine so pull that image
```bash
docker pull redis:7.4.2-alpine
```

- for data persistence let us create volumes for redis db (/data)
```bash
docker volume create redis0-data
docker volume create redis1-data
docker volume create redis2-data
```

- now run the redis.sh in storage folder, this should get 3 containers up and running 
```bash
cd storage/
bash redis.sh
cd ..
```

- to find the ip address of the sentinels run for all sentinels
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sentinel-0
```

- to run redis container interactively 
```bash
docker exec -it redis-0 redis-cli -h 172.18.0.2 -p 6379
```

- running the python container
```bash
docker run -t -v ${PWD}:/work -p 5000:5000 --net redis -e REDIS_SENTINELS="172.18.0.5:5000, 172.18.0.6:5000, 172.18.0.7:5000" -e REDIS_MASTER="mymaster" -e REDIS_PASSWORD="admin" flasker
```
