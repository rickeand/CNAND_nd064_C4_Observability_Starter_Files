kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.1/cert-manager.yaml

helm install prometheus prometheus-community/kube-prometheus-stack
#--kubeconfig /etc/rancher/k3s/k3s.yaml

kubectl create namespace observability
kubectl apply -f sampleapp/k8s/jaeger-operator.yaml
