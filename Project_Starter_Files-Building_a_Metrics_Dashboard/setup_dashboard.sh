#!/bin/bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml

kubectl create namespace monitoring
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring

kubectl create namespace observability
kubectl apply -f manifests/app/jaeger-operator.yaml

kubectl apply -f manifests/app/jaeger.yaml
kubectl apply -f manifests/app/backend.yaml
kubectl apply -f manifests/app/frontend.yaml
kubectl apply -f manifests/app/trial.yaml

ttab kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80

kubectl port-forward  service/simplest-query --address 0.0.0.0 16686:16686