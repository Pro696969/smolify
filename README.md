## Docker Containerization

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

---

## Container Orchestration - Kubernetes

- install [kind](https://kind.sigs.k8s.io/) (Kubernetes IN Docker) <br>
`kind is a tool for running local Kubernetes clusters using Docker container “nodes”. `

- Create a redis cluster
```bash
kind create cluster --name redis --image kindest/node:v1.23.5
```

- Apply the kind config so that flask-app ports get exposed properly
```bash
kind create cluster --config kind-config.yaml
```

- Create a namespace 
```bash
kubectl create ns redis
```

- We will be using the default storage class which is standard, you can check this by 
```bash
kind get storageclass
```


- Deployment of pods
    - Redis nodes (1 master 2 slaves)
        ```bash
        kubectl apply -n redis -f ./kubernetes/redis/redis-configmap.yaml
        kubectl apply -n redis -f ./kubernetes/redis/redis-statefulset.yaml
        ```
    - Redis Sentinel (3 instances)
        ```bash
        kubectl apply -n redis -f ./kubernetes/sentinel/sentinel-statefulset.yaml
        ```
    - Verify all pods are running 
        ```bash
        kubectl -n redis get pods
        ```
    You should see 3 redis pods and 3 sentinels so a total of 6 pods should be visible

    - Flask app (3 replicas)
        ```bash
        kubectl apply -f ./kubernetes/flask/flask-app-configmap.yaml
        kubectl apply -f ./kubernetes/flask/flask-app-secret.yaml
        kubectl apply -f ./kubernetes/flask/flask-app.yaml
        ```
        ```bash
        kubectl get pods # note that this is not inside redis namespace
        ```
    You should see 3 flask-app-{random hash} 

- Setting up metrics-server (the below command might take sometime so give it ~5mins)
```bash
kubectl apply -f .kubernetes/metrics-server/metrics-server-deployment.yaml
```
- To check if it got deployed correctly
```bash
kubectl get deployments -n kube-system
```
- Display resource (CPU/memory) usage of pods
```bash
kubectl top pods
```
```bash
kubectl describe hpa flask-app
```

- Port Forward local machine's port to the flask-app service 
```bash
kubectl port-forward service/flask-app 5000:5000 # (make sure to access app from http://127.0.0.1:30007/)
```

- Manual Monitoring
    - To check if flask app is receiving requests
        ```bash
        kubectl logs <flask-pod-name> # run for all pods one of them will be receiving requests
        ```
    - Interactively checking the redis db 
        ```bash
        kubectl -n redis exec -it redis-1 -- sh
        -> redis-cli
        -> auth admin
        -> keys *
        ```

- Logs of all flask-app pods
```bash
kubectl logs -l app=flask-app --prefix --follow --max-log-requests 10
```
## Stress Testing 

- Hitting the / end-point
```bash
bash stress-testing/stress_GET.sh
```
- Url-shortening
```bash
bash stress-testing/stress_POST.sh
```