# This script is used to create a Redis cluster with 3 master nodes and 3 sentinel nodes.

docker run -d --rm --name redis-0 --net redis -v ${PWD}/redis-0:/etc/redis/ -v redis0-data:/data redis:7.4.2-alpine redis-server /etc/redis/redis.conf
docker run -d --rm --name redis-1 --net redis -v ${PWD}/redis-1:/etc/redis/ -v redis1-data:/data redis:7.4.2-alpine redis-server /etc/redis/redis.conf
docker run -d --rm --name redis-2 --net redis -v ${PWD}/redis-2:/etc/redis/ -v redis2-data:/data redis:7.4.2-alpine redis-server /etc/redis/redis.conf


docker run -d --rm --name sentinel-0 --net redis -v ${PWD}/sentinel-0:/etc/redis/ redis:7.4.2-alpine redis-sentinel /etc/redis/sentinel.conf
docker run -d --rm --name sentinel-1 --net redis -v ${PWD}/sentinel-1:/etc/redis/ redis:7.4.2-alpine redis-sentinel /etc/redis/sentinel.conf
docker run -d --rm --name sentinel-2 --net redis -v ${PWD}/sentinel-2:/etc/redis/ redis:7.4.2-alpine redis-sentinel /etc/redis/sentinel.conf
