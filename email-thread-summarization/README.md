# email-thread-summarization

### Deploy
```
envsubst < examples-resources.yaml | kubectl apply -f -
```

### Build image
```
IMAGE=quay.io/ibm/ai-on-power-genai-email-thread-summarization
LABEL=v0.0.1
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```
