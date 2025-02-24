
# Multi Agent System deployment


### Overview
Welcome to the Multi-Agent System (MAS) Pipeline Deployment Guide. 
This comprehensive guide provides a step-by-step approach to deploying 
the MAS pipeline, covering everything from prerequisites to troubleshooting.

### What’s Included


- **Requirements**: A detailed list of necessary tools and configurations.
- **Deployment Commands**: All commands needed to successfully set up and run the pipeline.
- **Troubleshooting Notes**: Solutions to common issues encountered during deployment.

Follow this guide to ensure a seamless deployment process for the MAS pipeline.

### Requirements

- Kubernetes
- Docker
- Minikube

Start a new cluster with namespace 'desire6G' and enabled Container Network Interfaces (CNI)
```bash
minikube start --network-plugin=cni --namespace=desire6g
```

Create docker images and add them to the minikube repository
```bash
docker build -t desire6g/smo:latest . --no-cache 
docker build -t desire6g/mlfo:latest . --no-cache 
docker build -t desire6g/agent:latest . --no-cache 

minikube -p netherlands image load desire6g/smo:latest
minikube -p netherlands image load desire6g/mlfo:latest
minikube -p netherlands image load desire6g/agent:latest

eval $(minikube docker-env)
docker images
```


### References

- https://kubernetes.io/
- https://www.docker.com/
- https://minikube.sigs.k8s.io/docs/
- https://docs.tigera.io/calico/latest/getting-started/kubernetes/minikube
