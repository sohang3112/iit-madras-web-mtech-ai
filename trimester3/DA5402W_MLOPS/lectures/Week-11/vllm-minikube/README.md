# vLLM on Minikube

Self-hosted LLM inference using vLLM on a local minikube cluster.
Based on: https://www.cncf.io/blog/2026/07/16/running-a-self-hosted-llm-in-kubernetes-with-vllm/

Model: `meta-llama/Llama-3.2-1B-Instruct` (1B params, runs on CPU)

## Prerequisites

- minikube installed and running
- kubectl configured
- Hugging Face account with access to the Llama 3.2 model (request at https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)

## Start minikube with sufficient resources

```bash
minikube start --cpus=4 --memory=10240 --disk-size=60g
```

## Deploy

```bash
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-storage-and-secret.yaml
kubectl apply -f 02-deployment.yaml
kubectl apply -f 03-service.yaml
```

## Watch startup

First run downloads ~2.5 GB of model weights. Subsequent restarts use the cached PVC.

```bash
kubectl logs -f deployment/vllm-server -n vllm
```

Wait for: `Application startup complete`

## Test (in-cluster)

```bash
kubectl apply -f 04-curl-client.yaml
kubectl exec -it curl-client -n vllm -- sh

curl http://vllm-server.vllm.svc.cluster.local:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-1B-Instruct",
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

## Test (from host via NodePort)

```bash
minikube service vllm-server -n vllm --url
# Use the printed URL, e.g.:
curl http://192.168.49.2:31234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-1B-Instruct",
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

## Operations

```bash
# Pause (keeps cached model weights on PVC)
kubectl scale deployment vllm-server -n vllm --replicas=0

# Resume
kubectl scale deployment vllm-server -n vllm --replicas=1

# Cleanup
kubectl delete namespace vllm
```

## Prefix Caching Demo

The default deployment (`02-deployment.yaml`) has `--enable-prefix-caching` enabled.
To demonstrate the benefit:

### Run the demo with prefix caching ON (default)

```bash
kubectl apply -f 05-prefix-caching-demo.yaml
kubectl exec -it prefix-caching-demo -n vllm -- sh /scripts/run-demo.sh
```

The script sends multiple requests sharing a long system prompt and measures
time-to-response. With caching, requests 2+ reuse the KV-cache computed for the
shared prefix, reducing time-to-first-token significantly.

### Compare with prefix caching OFF

```bash
# Switch to the no-cache deployment
kubectl apply -f 02-deployment-no-prefix-cache.yaml
kubectl rollout status deployment/vllm-server -n vllm

# Re-run the same demo
kubectl exec -it prefix-caching-demo -n vllm -- sh /scripts/run-demo.sh
```

### Switch back to prefix caching ON

```bash
kubectl apply -f 02-deployment.yaml
kubectl rollout status deployment/vllm-server -n vllm
```

### What prefix caching does

| Scenario | Without caching | With caching |
|----------|----------------|--------------|
| Same system prompt, different user messages | Recomputes full KV every request | Computes system prompt KV once, reuses on subsequent requests |
| Multi-turn conversations | Full KV recomputation every turn | Only new tokens (latest turn) need KV computation |
| Concurrent requests with shared prefix | Each request pays full prefill cost | Shared prefix KV blocks are deduplicated in memory |

**When it helps most:**
- Long system prompts shared across many requests (RAG, agents, chatbots)
- Multi-turn conversations where history grows each turn
- High-concurrency serving where many users share the same base prompt

## Notes

- The Service uses `NodePort` (instead of ClusterIP from the blog) so you can hit the API from your host machine via `minikube service`.
- StorageClass is `standard` (minikube's default hostpath provisioner) instead of LINSTOR.
- Resource requests/limits are set for the CPU image — adjust if you add GPU support.
- The `--gpu-memory-utilization 0.80` flag is kept as vLLM uses it for memory reservation even on CPU.
