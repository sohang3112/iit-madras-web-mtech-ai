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

## Monitoring (Prometheus + Grafana)

### Prerequisites

- minikube cluster running (same one used for vLLM above)
- vLLM deployed and healthy (`kubectl get pods -n vllm` shows `vllm-server` Running)
- `kubectl` configured to target your minikube cluster

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  minikube cluster (namespace: vllm)                 │
│                                                     │
│  ┌──────────┐  scrape /metrics  ┌──────────────┐   │
│  │Prometheus├───────────────────►│ vLLM Server  │   │
│  │ :9090    │   every 15s       │ :8000        │   │
│  └────┬─────┘                   └──────────────┘   │
│       │                                             │
│       │ query                                       │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ Grafana  │                                       │
│  │ :3000    │                                       │
│  └──────────┘                                       │
└─────────────────────────────────────────────────────┘
```

### Install steps

1. **Ensure the vLLM namespace and server are running:**

   ```bash
   kubectl get ns vllm
   kubectl get pods -n vllm
   ```

   If not deployed yet, apply the base manifests first (see [Deploy](#deploy) above).

2. **Deploy Prometheus:**

   This creates a ConfigMap (scrape config), PVC (metric storage), Deployment, and NodePort Service in the `vllm` namespace.

   ```bash
   kubectl apply -f 07-prometheus.yaml
   ```

   Wait for it to be ready:

   ```bash
   kubectl rollout status deployment/prometheus -n vllm
   ```

3. **Deploy Grafana:**

   This creates ConfigMaps (datasource + dashboard provisioning + dashboard JSON), PVC, Deployment, and NodePort Service.

   ```bash
   kubectl apply -f 08-grafana.yaml
   ```

   Wait for it to be ready:

   ```bash
   kubectl rollout status deployment/grafana -n vllm
   ```

4. **Verify all pods are running:**

   ```bash
   kubectl get pods -n vllm
   ```

   Expected output:
   ```
   NAME                          READY   STATUS    RESTARTS   AGE
   vllm-server-xxx               1/1     Running   0          ...
   prometheus-xxx                 1/1     Running   0          ...
   grafana-xxx                    1/1     Running   0          ...
   ```

5. **Get the service URLs:**

   ```bash
   minikube service prometheus -n vllm --url
   minikube service grafana -n vllm --url
   ```

   Example output:
   ```
   http://192.168.49.2:31245   ← Prometheus
   http://192.168.49.2:30842   ← Grafana
   ```

   **Default URLs:**
   | Service | In-cluster URL | Host access |
   |---------|---------------|-------------|
   | Prometheus | `http://prometheus.vllm.svc.cluster.local:9090` | `http://<minikube-ip>:<nodeport>` |
   | Grafana | `http://grafana.vllm.svc.cluster.local:3000` | `http://<minikube-ip>:<nodeport>` |

   Get minikube's IP with: `minikube ip`

   Get the assigned NodePorts with:
   ```bash
   kubectl get svc -n vllm prometheus grafana
   ```

6. **Accessing from your local browser (when minikube runs in a VM):**

   If minikube is running inside a VM (e.g., VirtualBox, Hyper-V, QEMU, or a remote machine), the minikube IP is only reachable from the VM host network — not directly from your local browser. Use one of these methods:

   **Option A: `minikube tunnel` (recommended)**

   Run this in a separate terminal (keeps running in foreground):
   ```bash
   minikube tunnel
   ```
   This creates a network route from your local machine to the cluster's service IPs. You can then access Grafana at `http://localhost:3000` if using LoadBalancer-type services, or use the NodePort URL directly since the tunnel makes the minikube IP routable.

   **Option B: `kubectl port-forward` (simplest, works everywhere)**

   Forward Grafana to localhost:3000:
   ```bash
   kubectl port-forward svc/grafana 3000:3000 -n vllm
   ```

   Forward Prometheus to localhost:9090:
   ```bash
   kubectl port-forward svc/prometheus 9090:9090 -n vllm
   ```

   Then open in your browser:
   - Grafana: **http://localhost:3000**
   - Prometheus: **http://localhost:9090**

   **Option C: SSH tunnel (minikube on a remote machine)**

   If minikube is on a remote server you SSH into:
   ```bash
   # From your local machine — forward remote Grafana to local port 3000
   ssh -L 3000:<minikube-ip>:<grafana-nodeport> user@remote-server

   # From your local machine — forward remote Prometheus to local port 9090
   ssh -L 9090:<minikube-ip>:<prometheus-nodeport> user@remote-server
   ```

   Then open **http://localhost:3000** (Grafana) and **http://localhost:9090** (Prometheus) in your local browser.

   **Option D: `minikube service --url` with driver-specific access**

   For Docker driver on macOS/Windows (minikube runs in a Docker VM):
   ```bash
   minikube service grafana -n vllm
   ```
   This automatically opens a tunnel and prints a `http://127.0.0.1:<random-port>` URL that works from your host browser.

7. **Verify Prometheus is scraping vLLM:**

   Open the Prometheus URL in your browser, go to **Status > Targets**. You should see the `vllm` job with state `UP`.

   Or verify from the CLI:
   ```bash
   PROM_URL=$(minikube service prometheus -n vllm --url)
   curl -s "$PROM_URL/api/v1/targets" | python3 -m json.tool | grep -A2 '"health"'
   ```

7. **Log in to Grafana and view the dashboard:**

   Open the Grafana URL in your browser.
   - Username: `admin`
   - Password: `admin`
   - Skip the password change prompt (or set a new one)

   Navigate to **Dashboards > vLLM > "vLLM Inference Server"**.

   The dashboard will populate with data once you send requests to the vLLM server.

### What's monitored

| Panel | Metric | Description |
|-------|--------|-------------|
| KV Cache Utilization | `vllm:gpu_cache_usage_perc` | Percentage of KV cache blocks in use |
| Running Requests | `vllm:num_requests_running` | Requests currently being processed |
| Waiting Requests | `vllm:num_requests_waiting` | Requests queued waiting for KV cache space |
| E2E Request Latency | `vllm:e2e_request_latency_seconds` | End-to-end latency percentiles (p50/p95/p99) |
| Time to First Token | `vllm:time_to_first_token_seconds` | Time from request receipt to first generated token |
| Generation Tokens/sec | `vllm:generation_tokens_total` | Output token throughput |
| Prompt Tokens/sec | `vllm:prompt_tokens_total` | Input token processing rate |
| Prefix Cache Hit Rate | `vllm:prefix_cache_hit_total` | Ratio of cache hits to total prefix lookups |
| Inter-Token Latency | `vllm:inter_token_latency_seconds` | Time between consecutive generated tokens |
| Preemptions | `vllm:num_preemptions_total` | Rate of request preemptions due to memory pressure |

### Resource usage

The monitoring stack adds the following resource requirements to your minikube cluster:

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit | Storage |
|-----------|-------------|-----------|----------------|--------------|---------|
| Prometheus | 200m | 500m | 256Mi | 512Mi | 5Gi PVC |
| Grafana | 100m | 300m | 128Mi | 256Mi | 1Gi PVC |

Total additional: 300m CPU / 384Mi memory requested on top of the vLLM server.

### Cleanup

Remove only the monitoring stack (keeps vLLM running):

```bash
kubectl delete -f 08-grafana.yaml
kubectl delete -f 07-prometheus.yaml
```

To remove everything including stored metrics:

```bash
kubectl delete pvc prometheus-data grafana-data -n vllm
```

### Troubleshooting

- **No data in Grafana?** Metrics only appear after sending requests to vLLM. Send a test request and wait 15-30 seconds for Prometheus to scrape.
- **Prometheus target shows DOWN?** Check that the vLLM server pod is running and the service is reachable: `kubectl exec -it <prometheus-pod> -n vllm -- wget -qO- http://vllm-server:8000/metrics | head`
- **Grafana shows "No datasource"?** The provisioning may not have mounted correctly. Check: `kubectl logs deployment/grafana -n vllm | grep -i provision`
- **Metric names differ?** vLLM metric names can vary across versions. Run `curl $(minikube service vllm-server -n vllm --url)/metrics` to check the exact names and update the dashboard queries if needed.
- **Pods stuck in Pending?** Check if minikube has enough resources: `kubectl describe pod <pod-name> -n vllm` — you may need to increase minikube memory/CPU.

## Notes

- The Service uses `NodePort` (instead of ClusterIP from the blog) so you can hit the API from your host machine via `minikube service`.
- StorageClass is `standard` (minikube's default hostpath provisioner) instead of LINSTOR.
- Resource requests/limits are set for the CPU image — adjust if you add GPU support.
- The `--gpu-memory-utilization 0.80` flag is kept as vLLM uses it for memory reservation even on CPU.
