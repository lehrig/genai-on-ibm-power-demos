# selfservice-cust-assist-qna

```
IMAGE=quay.io/ibm/ai-on-power-genai-selfservice-cust-assist-qna
LABEL=v0.0.2
TAG=${IMAGE}:${LABEL}

docker buildx build -f Dockerfile -t ${TAG} --push . 
```
