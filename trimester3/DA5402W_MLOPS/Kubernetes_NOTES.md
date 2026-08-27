## Source: Directly from Lecture OR things I verified myself

Kubernetes (source: MLOps lecture slides of Week 9) :

`kubectl` acts as a client (runs commands against a Kubernetes cluser).
```bash
# Create a namespace
$ kubectl create namespace <urname>
# Go to the namespace:
$ kubectl config set-context --current --namespace=<namespacename>
```

For setting up a Kubernetes cluster locally use `minikube` which starts server.
It usually starts in some kind of a virtual environment, but leaves it to you to choose what ("pluggable drivers"): Docker, Podman, full VM or Bare Metal (no virtualization).

```bash
# on first run all commands take a bit of time due to downloading necessary components
# Install minikube
# Install kubectl
# Install docker/podman
$ minikube start --driver=docker         # start minikube inside a Docker
$ minikube kubectl create namespace abc
$ minikube kubectl  
```

"Kubernetes Pod" is a group of Docker containers with shared storage and network resources -- basically like Docker Compose, except that now the containers can be on different machines ("distributed") instead of Compose's constraint of a single machine running all the containers.

NOTE:  The YAML file given to `kubernetes apply` CAN include multiple YAML "documents" (seperated by ---) , though usually seperating all in seperate yaml files and applying them one by one is preferred.

```bash
# Create a single nginx pod:
$ kubectl apply -f ngnix-pod.yaml -n <namespace>
# Check the pod:
$ kubectl describe pod nginx
$ kubectl exec -it nginx -- /bin/bash
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx   # netshoot
      image: nginx  # nicola/netshoot
    # optional: command, args --> both list of strings 
    # can run a short bash code directly using /bin/bash -c "code"
      ports:        # optional
        - containerPort: 80

```

Kubernetes Deployment using Kubernetes Controllers features: (for pods) Rolling Updates, Rollbacks, Version Control:

```bash
# Replicas, delete and see them start
$ kubectl apply -f nginx_dep.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80

```

PersistentVolume is the actual host folder or disk you make available to the cluster, while a PersistentVolumeClaim is a Pod’s request to use a chunk of that storage. Both these are done via `kubectl` only. 

```bash
# Share your actual laptop folder into Minikube's VM
$ minikube mount /Users/you/project-data:/mnt/data
# Tell Kubernetes to use that directory as a PV
# generally with a series of kubernets apply different yaml files, order matters. each either creates its resource (if it doesn't exist), or modifies it if it exists already
kubectl apply -f pv.yaml   # (points to hostPath: /mnt/data)
# Request and attach that storage to your app
kubectl apply -f pvc.yaml
kubectl apply -f pod.yaml
```

Stateful Set, Daemon Set -- SKIPPED

Kubernetes Services has types:

1. ClusterIP: Default service type. Accessible within the cluster
2. NodePort: Allocates a port on each node to forward request to the service ; `--service-node-port-range` flag (default: 30000-32767)
3. Load Balancer: Traffic from the external load balancer is directed at the backend Pods. You can specify a loadBalancerIP or use ephemeral IP
4. ExternalName: Service to a DNS name. Eg. *my.database.example.com*
```bash
$ kubectl apply -f nginx-service.yaml
$ kubectl describe service nginx-service
# Check connectivity (use the netshoot pod)
$ `curl <serviceIP:port>`
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - port: 8765
      targetPort: 80
  type: LoadBalancer
```

Port forward: `kubectl port-forward -n ml-app svc/ml-app 8002:80`

Starting kubernetes GUI optionally:

```bash
$ minikube dashboard
🔌  Enabling dashboard ...
    ▪ Using image docker.io/kubernetesui/dashboard:v2.7.0
    ▪ Using image docker.io/kubernetesui/metrics-scraper:v1.0.8
💡  Some dashboard features require the metrics-server addon. To enable all features please run:

        minikube addons enable metrics-server

🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:38039/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...
```

Kubernetes Resources:

* https://github.com/pnl-iiitd/acm_fsn/tree/main (k8s and service)
* https://medium.com/aspnetrun/deploying-microservices-on-kubernetes-35296d369fdb

## Source: Gemini Chat re local Kubernetes setup (so something may possibly be wrong)

**Step-by-Step Bash Commands**

```bash
# 1. Start Minikube with isolated Docker driver (allocate enough resources)--> NOTE: start kubernetes cluster server in background, no need to keep terminal open
minikube start --driver=docker --cpus=4 --memory=6144

# 2. Point current shell's Docker CLI to Minikube's internal Docker daemon
eval $(minikube docker-env)

# 3. Build the training image directly inside Minikube's environment
docker build -t ml-training-image:latest -f docker/Dockerfile.train .

# 4. Apply Kubernetes manifests in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/training-job.yaml

# 5. Monitor Job execution and stream training logs
kubectl -n ml-training get pods -w
kubectl -n ml-training logs -f job/ml-training-job

# --- Optional / Cleanup ---
# Unset the Minikube Docker environment in your current shell
eval $(minikube docker-env -u)

# Delete the Minikube cluster when finished
minikube delete
```

* **Host Pollution with the `none` Driver:** (due to which `docker` driver preferred -- ie `minikube` runs everything needed by cluster inside docker).
`kubectl` is just a client CLI. The `none` (bare-metal) driver pollutes your host OS by installing cluster system processes (`kubelet`, `kubeadm`), modifying `/opt/cni/bin/`, rewriting host `iptables`, and creating root directories (`/var/lib/kubelet`, `/etc/kubernetes`). The Docker driver keeps everything contained in a single container.
* **Purpose of `eval $(minikube docker-env)`:**
It runs in your host terminal and temporarily sets environment variables (like `DOCKER_HOST`) so your standard `docker build` commands talk directly to Minikube's internal Docker daemon instead of your host machine's daemon.
* **Container-in-Container Concerns:**
While Docker-in-Docker has a bad reputation in CI/production due to layered storage conflicts and security risks, Minikube and Kubernetes-in-Docker are specifically engineered to use modern kernel drivers safely. For local assignments, it provides a clean, disposable sandbox that you can wipe completely with `minikube delete`.

Order matters of `kubernetes apply -f FILENAME.yaml`, because each level has to first create a resource needed by next level.
As a general rule of thumb:

| Order | Resource Category       | Examples                                  | Purpose                                               |
| ----- | ----------------------- | ----------------------------------------- | ----------------------------------------------------- |
| 1     | Scope & Access          | Namespace, CRDs, RBAC (Role, RoleBinding) | Creates the container boundary and permissions.       |
| 2     | Storage & Configuration | ConfigMap, Secret, PersistentVolumeClaim  | Provides inputs and disk space required by workloads. |
| 3     | Workloads               | Job, Deployment, StatefulSet, DaemonSet   | The actual containers running your code.              |
| 4     | Networking & Routing    | Service, Ingress                          | Exposes workload endpoints.                           |
