# pii-extraction

### Deploy
```
export CLUSTER_DOMAIN=$(oc get ingresses.config/cluster -o jsonpath={.spec.domain})
envsubst < examples-resources.yaml | kubectl apply -f -
```

### Build image
```
IMAGE=quay.io/ibm/ai-on-power-genai-pii-extraction
LABEL=v0.0.1
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```
