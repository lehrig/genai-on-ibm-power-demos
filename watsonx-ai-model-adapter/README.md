# watsonx-ai-model-adapter

### Deploy
```
export CLUSTER_DOMAIN=$(oc get ingresses.config/cluster -o jsonpath={.spec.domain})
export HUGGING_FACE_TOKEN=hf_yourtoken
export LLM_NODE=$(oc get node -o jsonpath={.items[0].metadata.name})
export MODEL=google/flan-t5-base
export VIRTUAL_CPUS=64
envsubst < examples-resources.yaml | kubectl apply -f -
```

### Build image
```
IMAGE=quay.io/ibm/ai-on-power-genai-watsonx-ai-model-adapter
LABEL=v0.0.11
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```

