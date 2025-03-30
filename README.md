###### working basic redis

- docker pull redis
- docker run -it --rm --name redis --net redis -p 6969:6379 redis   // redis server
- docker exec -it redis redis-cli                                   // redis client 

---

