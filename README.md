# Generative AI demos on IBM Power
Demos featuring generative AI capabilities on IBM Power. Based on watsonx demos from https://github.com/IBM/dsce-sample-apps. Run on IBM Power10 for using large language models (LLMs) with low latency and without requiring GPUs.

## Pre-requisites

### Install Kustomize
```
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

## Deploy to Red Hat OpenShift
```
export CLUSTER_DOMAIN=$(oc get ingresses.config/cluster -o jsonpath={.spec.domain})
# specify Huggig Face token for models requiring login (e.g., meta/Llama2)
export HUGGING_FACE_TOKEN=hf_yourtoken
export LLM_NODE=$(oc get node -o jsonpath={.items[0].metadata.name})
# Optional: hard code targeted LLM node
#export LLM_NODE=p114worker04.b2s001.pbm.ihost.com
export MODEL=google/flan-t5-base
export VIRTUAL_CPUS=64

./kustomize build | envsubst '${CLUSTER_DOMAIN}' | envsubst '${HUGGING_FACE_TOKEN}' | envsubst '${LLM_NODE}' | envsubst '${MODEL}' | envsubst '${VIRTUAL_CPUS}' | awk '!/well-defined/' | oc apply -f -
```

## Access demos
Goto:
- http://brief-builder-demos.$CLUSTER_DOMAIN/brief-builder/
- http://conversation-intelligence.$CLUSTER_DOMAIN/conversation-intelligence/
- http://email-thread-summarization.$CLUSTER_DOMAIN/email-thread-summarization/
- http://privacy-compliance.$CLUSTER_DOMAIN/privacy-compliance/
- http://selfservice-cust-assistant.$CLUSTER_DOMAIN/selfservice-cust-assistant/

