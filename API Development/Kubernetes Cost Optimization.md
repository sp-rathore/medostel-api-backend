# Medostel Kubernetes Cluster - Cost Optimization Strategy

## Overview

This document outlines comprehensive cost optimization strategies for the medostel-api-cluster in Google Kubernetes Engine (GKE).

---

## Current Configuration vs Optimized Configuration

### Before Optimization

| Component | Specification | Monthly Cost |
|-----------|---------------|--------------|
| **Node Pool** | Standard e2-medium (SSD) | $63.88 |
| **Max Nodes** | 5 | ~$25.50 |
| **Storage** | SSD (pd-ssd) | $17.85 |
| **Load Balancer** | Yes | $18-20 |
| **Network Egress** | 200 GB | $23.88 |
| **Logging** | Full ingestion | $10.00 |
| **TOTAL** | | **$159.11** |

### After Optimization

| Component | Specification | Monthly Cost |
|-----------|---------------|--------------|
| **Standard Pool** | Standard e2-medium (HDD) | $31.50 |
| **Preemptible Pool** | Preemptible e2-medium (HDD) | $12.60 |
| **Max Nodes** | 3 standard + 2 preemptible | $15.00 |
| **Storage** | HDD (pd-standard) | $4.50 |
| **Load Balancer** | Yes (fixed) | $18.00 |
| **Network Egress** | 200 GB (optimized) | $23.88 |
| **Logging** | Sampled (50%) | $5.00 |
| **TOTAL** | | **$110.48** |

**Total Savings: ~31% monthly cost reduction**

---

## Optimization Strategies Implemented

### 1. Preemptible Nodes (60% Cheaper)

**What**: Short-lived VM instances that Google can interrupt
**Savings**: ~60% discount on compute costs
**Best For**: Non-critical workloads, batch processing, dev/test

```yaml
apiVersion: v1
kind: NodePool
metadata:
  name: preemptible-pool
spec:
  machineType: e2-medium
  diskType: pd-standard  # HDD instead of SSD
  preemptible: true
  autoscaling:
    minNodes: 2
    maxNodes: 3
```

**Implementation**:
```bash
gcloud container node-pools create preemptible-pool \
  --cluster=medostel-api-cluster \
  --region=asia-south1 \
  --preemptible \
  --machine-type=e2-medium \
  --disk-type=pd-standard \
  --min-nodes=2 \
  --max-nodes=3
```

**How to Use in Deployments**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medostel-api
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: cloud.google.com/gke-preemptible
                    operator: In
                    values:
                    - "true"
      tolerations:
      - key: cloud.google.com/gke-preemptible
        operator: Equal
        value: "true"
        effect: NoSchedule
```

### 2. Switch from SSD to HDD Storage (75% Savings)

**Current**: pd-ssd (SSD) @ $0.17/GB/month
**Optimized**: pd-standard (HDD) @ $0.04/GB/month
**Savings**: 75% storage cost reduction

```bash
# New nodes use HDD automatically
# Existing SSD nodes can be gradually replaced
gcloud container node-pools create standard-hdd-pool \
  --cluster=medostel-api-cluster \
  --region=asia-south1 \
  --machine-type=e2-medium \
  --disk-type=pd-standard \
  --disk-size=30
```

### 3. Reduce Maximum Nodes (20% Reduction)

**Before**: min=2, max=5
**After**:
- Standard pool: min=2, max=3
- Preemptible pool: min=1, max=2

```bash
gcloud container clusters update medostel-api-cluster \
  --region=asia-south1 \
  --project=gen-lang-client-0064186167 \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=3
```

### 4. Log Sampling & Filtering (50% Logging Cost Reduction)

Reduce Cloud Logging costs by sampling non-critical logs:

```yaml
# fluent-bit-config.yaml - Log sampling configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: kube-system
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush        5
        Log_Level    info
        Parsers_File parsers.conf

    [INPUT]
        Name              tail
        Path              /var/log/containers/*medostel*.log
        Parser            docker
        Tag               kube.*
        Refresh_Interval  5

    [FILTER]
        Name    sampling
        Match   kube.*
        sample  2  # Log 1 out of every 2 messages

    [OUTPUT]
        Name  stackdriver
        Match *
```

Deploy:
```bash
kubectl apply -f fluent-bit-config.yaml
```

### 5. Resource Quotas & Limits (Prevent Waste)

Implement resource quotas to prevent over-provisioning:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: medostel-quota
  namespace: medostel-api
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "20"
    services.loadbalancers: "1"

---

apiVersion: v1
kind: LimitRange
metadata:
  name: medostel-limits
  namespace: medostel-api
spec:
  limits:
  - max:
      cpu: "500m"
      memory: "512Mi"
    min:
      cpu: "50m"
      memory: "64Mi"
    type: Container
```

Deploy:
```bash
kubectl apply -f resource-quotas.yaml
```

### 6. Committed Use Discounts (CUDs) - 25-30% Savings

Purchase 1-year or 3-year commitments for compute resources:

```bash
# Via Console: Billing → Committed Use Discounts
# Or via gcloud:
# Note: This is typically done through the Cloud Console
```

**Estimated Savings**:
- 1-year CUD: 25% discount
- 3-year CUD: 30% discount

**Cost Impact**:
- Current: $44.10/month for compute
- With 3-year CUD: $30.87/month (30% savings)
- **Monthly savings: $13.23**

---

## Pod Optimization Configuration

### Optimized Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medostel-api-optimized
  namespace: medostel-api
spec:
  replicas: 2  # Reduced from 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: medostel-api
  template:
    metadata:
      labels:
        app: medostel-api
    spec:
      # Use preemptible nodes
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: cloud.google.com/gke-preemptible
                operator: In
                values:
                - "true"
      tolerations:
      - key: cloud.google.com/gke-preemptible
        operator: Equal
        value: "true"
        effect: NoSchedule

      serviceAccountName: medostel-api

      # Pod disruption budget for graceful handling of preemptions
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - medostel-api
              topologyKey: kubernetes.io/hostname

      containers:
      - name: api
        image: gcr.io/gen-lang-client-0064186167/medostel-api:latest
        imagePullPolicy: IfNotPresent

        # Resource limits for cost control
        resources:
          requests:
            cpu: 100m          # Minimum 100m CPU
            memory: 128Mi      # Minimum 128Mi memory
          limits:
            cpu: 200m          # Maximum 200m CPU
            memory: 256Mi      # Maximum 256Mi memory

        ports:
        - name: http
          containerPort: 8000

        env:
        - name: DB_HOST
          value: "35.200.195.16"
        - name: DB_PORT
          value: "5432"
        - name: DB_NAME
          value: "medostel"
        - name: DB_USER
          value: "medostel_api_user"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password

        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3

---

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: medostel-api-hpa
  namespace: medostel-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: medostel-api-optimized
  minReplicas: 2
  maxReplicas: 5  # Reduced from 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30

---

apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: medostel-api-pdb
  namespace: medostel-api
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: medostel-api
```

---

## Monitoring & Optimization

### Set Up Budget Alerts

```bash
# Create budget alert in Cloud Console or via API
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Medostel K8s Budget" \
  --budget-amount=150 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=100
```

### Monitor Cluster Costs

```bash
# View costs by resource
gcloud billing accounts list --format=json

# Monitor node costs
kubectl top nodes

# Monitor pod resource usage
kubectl top pods -A

# Check resource requests vs actual usage
kubectl describe nodes
kubectl describe pods -n medostel-api
```

### Cost Dashboard Query

```bash
# BigQuery query to analyze GCP costs
SELECT
  service.description,
  ROUND(SUM(cost), 2) as total_cost,
  ROUND(SUM(usage.amount), 2) as usage_amount,
  usage.unit
FROM `PROJECT_ID.billing_export_dataset.gcp_billing_export_v1`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND resource.labels.cluster_name = 'medostel-api-cluster'
GROUP BY 1, 4
ORDER BY total_cost DESC
```

---

## Optimization Checklist

- [x] Create preemptible node pool
- [x] Switch to HDD storage (pd-standard)
- [x] Reduce max nodes to 3 (standard) + 2 (preemptible)
- [ ] Apply resource quotas and limits
- [ ] Configure log sampling
- [ ] Purchase 1-year Committed Use Discount
- [ ] Deploy cost-optimized pods
- [ ] Set up budget alerts
- [ ] Configure monitoring dashboard
- [ ] Implement cost tracking
- [ ] Review monthly bills
- [ ] Auto-scale during off-peak hours

---

## Cost Projection - With All Optimizations

### Monthly Breakdown (Optimized)

| Component | Calculation | Cost |
|-----------|-------------|------|
| **Compute (Standard)** | 2 nodes × $0.0176/hr × 730 hrs | $25.70 |
| **Compute (Preemptible)** | 1.5 nodes × $0.0070/hr × 730 hrs | $7.67 |
| **Storage** | 105 GB × $0.04/GB (HDD) | $4.20 |
| **Load Balancer** | Fixed | $18.00 |
| **Network Egress** | 200 GB × $0.12/GB | $23.88 |
| **Logging** | Sampled 50% | $5.00 |
| **Subtotal** | | $84.45 |
| **With 3-yr CUD (30%)** | $84.45 × 0.70 | **$59.12** |

**Total Savings: 63% from original estimate**

---

## Scaling Cost Scenarios

### Light Traffic (1 node standard + 1 preemptible)
```
Monthly: ~$45-55
```

### Medium Traffic (2 standard + 1 preemptible)
```
Monthly: ~$59-75
```

### High Traffic (3 standard + 2 preemptible, auto-scaled)
```
Monthly: ~$110-130
```

### Peak Traffic (3 standard + 3 preemptible)
```
Monthly: ~$150-180
```

---

## Implementation Timeline

**Phase 1 (Immediate)**: Preemptible nodes, HDD storage
- **Time**: 1-2 hours
- **Savings**: 40-50%

**Phase 2 (Week 1)**: Resource quotas, log sampling
- **Time**: 2-4 hours
- **Savings**: Additional 5-10%

**Phase 3 (Month 1)**: Committed Use Discounts
- **Time**: 30 minutes
- **Savings**: Additional 25-30%

**Phase 4 (Ongoing)**: Monitoring and optimization
- **Time**: Weekly reviews
- **Savings**: Continuous 5-10%

---

## Risk Mitigation

### Preemptible Node Risks
```
Mitigation Strategy:
1. Use Pod Disruption Budgets (PDB)
2. Multiple replicas across zones
3. Quick pod startup time
4. Proper graceful shutdown handling
```

### Storage Performance
```
HDD vs SSD Impact:
- Application latency: +5-15ms (acceptable for most APIs)
- Throughput: Sufficient for 90% of use cases
- Cost savings: 75%

Recommendation: Use HDD for development, consider SSD for production if needed
```

---

## Conclusion

With the implemented optimizations, the Medostel Kubernetes cluster can achieve:

✅ **63% cost reduction** (from $159 to $59/month)
✅ **Automatic scaling** based on demand
✅ **High availability** with proper configuration
✅ **Production-ready** security and monitoring
✅ **Flexible** to scale based on traffic

**Next Step**: Apply these optimizations and monitor the actual costs during the first month.

---

**Last Updated**: 2026-02-28
**Status**: Ready for Implementation
**Estimated Savings**: $100/month (63% reduction)
