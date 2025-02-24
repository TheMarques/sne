#!/bin/bash
set -ex

# Verify that required commands are available.
which kubectl
which minikube

# Load environment variables (e.g. CLUSTER and CLUSTER2).
# source .env

for cluster in cluster cluster-2; do #$CLUSTER $CLUSTER2; do
  echo "=== Starting Minikube profile '$cluster' with Calico ==="

  namespace=development
  # Start the Minikube cluster with the Docker driver.
  # The --cni flag can be used to install Calico automatically,
  # but here we install our own version below.
  minikube start -v=1 --driver=docker --profile="$cluster" --cni=calico --namespace=$namespace

  # List local Docker images.
  docker images

  # Create or update the desired namespace.
  # kubectl apply -f namespace.yaml

  # (Optional) Launch the Minikube dashboard in the background.
  # minikube dashboard --profile="$cluster" &

  # Switch kubectl context to the current cluster profile.
  kubectl config use-context "$cluster"

  kubectl create namespace $namespace || echo "namespace $namespace already exists."

  #echo "=== Installing Calico on cluster '$cluster' ==="
  # Install Calico from the official manifest.
  #kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.1/manifests/calico.yaml

  #echo "=== Waiting for Calico pods to be ready on cluster '$cluster' ==="
  # Wait until the Calico daemonset is fully rolled out.
  #kubectl rollout status daemonset/calico-node -n kube-system --timeout=120s

  #echo "=== Patching Calico IPPool for VXLAN mode on cluster '$cluster' ==="
  # Patch the default IPPool to disable IPIP and enable VXLAN.
  #kubectl patch ippool default-ipv4-ippool \
  #  --patch '{"spec": {"vxlanMode": "Always", "ipipMode": "Never"}}' \
  #  --type=merge

  # Install your helm charts for each application.
  for dir in agent mlfo smo network-function; do
      echo "Applying resources in '$dir' on cluster '$cluster'..."
      helm install "$dir" "$dir/$dir-0.1.0.tgz" --namespace=$namespace
  done

  # List profiles and show resources in the desire6g namespace.
  # minikube profile list
  kubectl get all --namespace=$namespace
done

minikube profile list

echo "All resources applied successfully!"
