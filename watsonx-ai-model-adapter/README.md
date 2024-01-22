# watsonx-ai-model-adapter

### Deploy
```
export HUGGING_FACE_TOKEN=hf_yourtoken
envsubst < examples-resources.yaml | kubectl apply -f -
```

### Build image
```
IMAGE=quay.io/ibm/ai-on-power-genai-watsonx-ai-model-adapter
LABEL=v0.0.5
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```

