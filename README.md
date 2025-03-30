###### working basic redis

- docker pull redis
- docker run -it --rm --name redis --net redis -p 6969:6379 redis   // redis server
- docker exec -it redis redis-cli                                   // redis client 

---

##### redis clustering

- making use of redis sentinel for high availability

###### how to setup

- ensure you are using the same network across to do this 
```docker network create redis```

- you will need redis:7.4.2-alpine so pull that image
`docker pull redis:7.4.2-alpine`

- now run the redis.sh in storage folder, this should get 3 containers up and running 
`cd storage/`
`bash redis.sh`
`cd ..`

- to find the ip address of the sentinels run for all sentinels
`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sentinel-0`

- to run redis container interactively 
`docker exec -it sentinel-0 redis-cli -h 172.18.0.4 -p 6379`

- running the python container
`docker run -t -v ${PWD}:/work -p 5000:5000 --net redis -e REDIS_SENTINELS="172.18.0.5:5000, 172.18.0.6:5000, 172.18.0.7:5000" -e REDIS_MASTER="mymaster" -e REDIS_PASSWORD="admin" flasker`
