# ML Ops Pytorch Pipeline

The project implements a complete local MLOps workflow around a CIFAR-10 image classifier. The model is a simple PyTorch CNN. Training uses hyperparameters supplied in *configs/training_config.yaml*. The trained model *checkpoints/classifier_v1.pt* is tracked with Git LFS.

Flow is Training -> Prediction Server (using FastAPI). Whole thing is done using Kubernetes local cluster setup.

* **Github Repo Link**: https://github.com/sohang3112/mlops-pytorch-pipeline  (main branch) ---> See README.md of the repo for install & run details.
* **Last Pull Request (having Kubernetes End-to-End Workflow Log text)**: https://github.com/sohang3112/mlops-pytorch-pipeline/pull/4

4 Pull Requests in Github were done during development (using feature branches):

1. (Week 1) Directly train CNN model and serve it on Fastapi server -- https://github.com/sohang3112/mlops-pytorch-pipeline/pull/1
2. (Week 1) Implement Docker Containerization of train and serve -- https://github.com/sohang3112/mlops-pytorch-pipeline/pull/2
3. (Week 2) Setup Kubernetes local cluster & do training -- https://github.com/sohang3112/mlops-pytorch-pipeline/pull/3
4. (Week 2) Run fastapi server in Kubernetes and record end-to-end workflow logs -- https://github.com/sohang3112/mlops-pytorch-pipeline/pull/4

## Most Challenging Part: Kubernetes Setup, Training, and Serving

The most challenging part of this project was Kubernetes, covering the initial local-cluster setup, the training Job, and the serving Deployment. The Pytorch model itself and the FastAPI endpoint were comparatively direct to build and test locally. Kubernetes felt very different because a working application depended on several layers agreeing at once: Minikube, Docker images, Kubernetes manifests, volumes, permissions, paths, resources, and networking. When one layer was corrected, the next issue often became visible, so debugging felt never-ending.

The first challenge was understanding that Minikube is its own environment. Images built on the host are not automatically usable by the cluster, and paths on the host are not automatically paths inside Minikube. The final workflow therefore builds images using Minikube's Docker environment and mounts the project directory into the Minikube VM. This made it possible for the training Job to use the cached CIFAR-10 data through a `hostPath` volume, but it also required being precise about the VM path rather than assuming the host path would work.

Training introduced another set of interconnected problems. The Job needed configuration, data, and a location to save the model checkpoint. A ConfigMap supplied the training YAML, while a PVC carried the checkpoint from training to serving. File ownership and write permissions became especially important because the images deliberately run as a non-root user. The solution included an init container that creates the checkpoint directory and adjusts its permissions. Resource settings and reducing DataLoader workers were also necessary to make the CPU-only local cluster run reliably rather than encountering difficult-to-diagnose memory or process problems.

Serving was not merely a matter of starting FastAPI in a Pod. The Deployment had to mount the same checkpoint location read-only, wait until the application was ready, and expose two replicas through a Service whose selector matched the Pod labels. Health, liveness, and readiness probes were needed so Kubernetes could distinguish a running container from a usable prediction API. Kubernetes problems faced are basically integration problems. During the process I had to learn how to inspect (for debugging) in Kubernetes: Pod status, logs, mounted files, permissions, image availability, and network exposure.
