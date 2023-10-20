# watsonx-ai-model-adapter

```
IMAGE=quay.io/ibm/ai-on-power-genai-watsonx-ai-model-adapter
LABEL=v0.0.1
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```
