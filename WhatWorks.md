## Week 1: Develop and containerize the basic URL shortener service.
- Task 1: Write a simple Python or Node.js application to:
    - Accept long URLs via an API. ✅
    - Generate a short URL. ✅
    - Redirect users from short URLs to the original long URLs. ✅
- Task 2: Use an in-memory key-value store (e.g., Redis or a dictionary in Python) to
store URL mappings. ✅
- Task 3: Write a Dockerfile and build a Docker container for the application. ✅
- Task 4: Test the containerized app locally using docker run. ✅

## Week 2: Deploy the application on Kubernetes and configure networking.
- Task 1: Write Kubernetes Deployment & Service manifests for:
    - URL Shortener Pod (runs multiple instances of the app). ✅
    - Key-Value Store Pod (stores shortened URLs). ✅
    - ClusterIP Service to expose the key-value store internally. ✅
    - LoadBalancer/NodePort Service to expose the URL shortener. ✅
- Task 2: Deploy the application on Kubernetes using kubectl apply. ✅
- Task 3: Test the API with multiple instances running. ✅
- Task 4: Implement Kubernetes ConfigMaps & Secrets for managing environment
variables. ✅

## Week 3: Make the system scalable and fault-tolerant.
-  Task 1: Set up Kubernetes Horizontal Pod Autoscaler (HPA) to scale based on CPU usage. ✅
-  Task 2: Implement Kubernetes Ingress or a LoadBalancer for better traffic routing. 
-  Task 3: Configure Kubernetes Logs and kubectl get pods / logs for monitoring.
-  Task 4: Conduct stress testing to see how the system scales under load.