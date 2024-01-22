# watsonx-ai-model-adapter

### Deploy
```
export MODEL=google/flan-t5-base
export HUGGING_FACE_TOKEN=hf_yourtoken
envsubst < examples-resources.yaml | kubectl apply -f -
```

### Build image
```
IMAGE=quay.io/ibm/ai-on-power-genai-watsonx-ai-model-adapter
LABEL=v0.0.6
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```

