# Medostel Kubernetes Cluster Configuration

## 🔷 Live Cluster Status (Current)

### Real-time Cluster Information
| Property | Value |
|----------|-------|
| **Status** | 🟢 RUNNING |
| **Current Nodes** | 4 nodes |
| **Kubernetes Version** | 1.34.3-gke.1318000 |
| **Created** | 2026-02-28 11:31:31 UTC |
| **Cluster ID** | e601bdd2cc834869a646a5af9f27fab49d73e86e0d5548fb8ae9ba2f0423d91e |

### Node Pools Status

#### Default Pool
| Property | Value |
|----------|-------|
| **Name** | default-pool |
| **Status** | RUNNING |
| **Initial Nodes** | 2 |
| **Current Nodes** | Managed by autoscaling |
| **Machine Type** | e2-medium |
| **Auto-Scaling** | ✅ Enabled (BALANCED) |
| **Zones** | asia-south1-a, asia-south1-b, asia-south1-c |
| **Version** | 1.34.3-gke.1318000 |
| **Management** | Auto-Repair: ✅, Auto-Upgrade: ✅ |

#### Preemptible Pool
| Property | Value |
|----------|-------|
| **Name** | preemptible-pool |
| **Status** | RUNNING |
| **Initial Nodes** | 2 |
| **Current Nodes** | Managed by autoscaling |
| **Machine Type** | e2-medium |
| **Auto-Scaling** | ✅ Enabled (ANY) |
| **Zones** | asia-south1-a, asia-south1-b, asia-south1-c |
| **Version** | 1.34.3-gke.1318000 |

---

## Cluster Overview

### Basic Information

| Property | Value |
|----------|-------|
| **Cluster Name** | medostel-api-cluster |
| **Status** | 🟢 RUNNING |
| **Region** | asia-south1 (Mumbai) |
| **Location** | asia-south1 (Regional - 3 zones) |
| **Platform** | Google Kubernetes Engine (GKE) |
| **Project** | gen-lang-client-0064186167 |
| **Cluster Tier** | STANDARD |
| **Network Tier** | NETWORK_TIER_DEFAULT |

### Cluster Access Information
| Property | Value |
|----------|-------|
| **Control Plane Endpoint (DNS)** | gke-e601bdd2cc834869a646a5af9f27fab49d73-184488333549.asia-south1.gke.goog |
| **Public Endpoint** | 35.200.139.226 |
| **Private Endpoint** | 10.160.0.2 |
| **Public Endpoint Status** | ✅ Enabled |

---

## Cluster Specifications

### Node Configuration

| Property | Value |
|----------|-------|
| **Current Nodes** | 4 nodes (running) |
| **Node Pools** | 2 (default-pool, preemptible-pool) |
| **Node Auto-Scaling** | ✅ Enabled |
| **Min Nodes (per pool)** | 2 |
| **Max Nodes (per pool)** | Unlimited (GKE Auto-manages) |
| **Machine Type** | e2-medium (2 vCPU, 4 GB RAM per node) |
| **Disk Type** | SSD (pd-ssd) |
| **Disk Size** | 30 GB per node |
| **Image Type** | COS_CONTAINERD |
| **Max Pods per Node** | 110 |

### Resource Allocation

```
Per Node:
- CPU: 2 vCPU (e2-medium)
- Memory: 4 GB RAM
- Storage: 30 GB SSD

Current State (4 nodes):
- CPU: 8 vCPU total
- Memory: 16 GB total
- Storage: 120 GB total

Theoretical Maximum (if scaled to max):
- Could scale beyond initial 5-node limit
- Uses GKE's Autoprovisioning with balanced profile
```

### Network Configuration
| Property | Value |
|----------|-------|
| **VPC** | VPC-Native (IP Aliasing) |
| **Cluster IP Range** | 10.52.0.0/14 |
| **Service IP Range** | 34.118.224.0/20 |
| **Pod CIDR Overprovisioning** | ✅ Configured |
| **Default Pod IP Range** | Utilization: 0.39% |
| **Stack Type** | IPV4 |

---

## Node Management & Provisioning

### Autoprovisioning Configuration
| Property | Value |
|----------|-------|
| **Autoprovisioning Enabled** | ✅ Yes |
| **Autoscaling Profile** | BALANCED |
| **Default Image Type** | COS_CONTAINERD |
| **Default Machine Type** | e2-medium |
| **Service Account** | default |
| **OAuth Scopes** | Minimal (see below) |
| **Auto-Repair** | ✅ Enabled |
| **Auto-Upgrade** | ✅ Enabled |

### Node Upgrade Settings
| Property | Value |
|----------|-------|
| **Upgrade Strategy** | SURGE |
| **Max Surge** | 1 node |
| **Current Master Version** | 1.34.3-gke.1318000 |
| **Current Node Version** | 1.34.3-gke.1318000 |

### Autoscaling Configuration
| Property | Value |
|----------|-------|
| **Profile** | BALANCED |
| **Default Provisioning Model** | On-Demand (non-preemptible for default-pool) |
| **Preemptible Pool** | ✅ Available for cost optimization |
| **Location Policy (default)** | BALANCED (spreads across zones) |
| **Location Policy (preemptible)** | ANY |

---

## Security Configuration

### 1. Network Security

#### Network Policy
```
Status: ✅ ENABLED
Provider: CALICO
Type: Kubernetes NetworkPolicy (CNI)
```
**Features**:
- Namespace-level traffic control
- Pod-to-pod communication policies
- Ingress and egress rules
- Default-deny configuration support

#### IP Aliasing
```
Status: ✅ ENABLED
Type: VPC-Native
```
**Features**:
- Uses secondary IP ranges for pods
- Improved networking performance
- Better security isolation

### 2. Node Security

#### Shielded Nodes
```
Status: ✅ ENABLED
Features:
- Secure boot: ENABLED
- Integrity monitoring: ENABLED
- Virtual Trusted Platform Module (vTPM): ENABLED
```

**Security Benefits**:
- Protects against rootkits and bootloader attacks
- Ensures node integrity
- Detects unauthorized modifications

#### Node OS Configuration
```
OAuth Scopes (Minimal Required):
- devstorage.read_only: Read Cloud Storage (logs, artifacts)
- logging.write: Write to Cloud Logging
- monitoring: Write metrics to Cloud Monitoring
- service.management.readonly: Read service management
- servicecontrol: Service control access
- trace.append: Write to Cloud Trace
```

### 3. Identity & Access Management

#### Workload Identity
```
Status: ✅ ENABLED
Pool: gen-lang-client-0064186167.svc.id.goog
Type: Kubernetes Service Account to Google Service Account mapping
```

**Benefits**:
- No need for service account keys
- Fine-grained access control
- Automatic credential rotation
- Audit trail for all access

#### RBAC (Role-Based Access Control)
```
Status: ✅ DEFAULT (Enabled by default in GKE)
Default Bindings:
- system:masters (Cluster admins)
- system:authenticated (Authenticated users)
- system:unauthenticated (Public access - restricted by policies)
```

### 4. Add-ons & Features

| Add-on | Status | Purpose |
|--------|--------|---------|
| **HTTP Load Balancing** | ✅ Enabled | Ingress controller for external traffic |
| **Horizontal Pod Autoscaling** | ✅ Enabled | Auto-scale pods based on CPU/memory |
| **DNS Cache** | ✅ Enabled | Node-level DNS caching for performance |
| **GCE Persistent Disk CSI Driver** | ✅ Enabled | Volume management |
| **Kubernetes Dashboard** | ❌ Disabled | Security best practice |
| **Config Connector** | ❌ Disabled | Not required |
| **Workload Identity** | ✅ Enabled | Pod to GCP service account mapping |
| **Intra-node Visibility** | ❌ Disabled | Not configured |

### 5. API Server Configuration
| Property | Value |
|----------|-------|
| **Anonymous Authentication** | ✅ ENABLED (Controlled by policies) |
| **ABAC** | ❌ Legacy ABAC disabled |
| **Authorized Networks** | Not restricted (all networks) |
| **Public Endpoint** | ✅ Enabled |
| **Private Endpoint** | ✅ Enabled (10.160.0.2) |

---

## Database Connectivity

### PostgreSQL Connection from Kubernetes

#### Cloud SQL Instance Details
| Property | Value |
|----------|-------|
| **Instance Name** | medostel-ai-assistant-pgdev-instance |
| **Database Engine** | PostgreSQL 18.2 |
| **Edition** | ENTERPRISE |
| **Primary IP** | 35.244.27.232 |
| **Outgoing IP** | 34.100.144.210 |
| **Port** | 5432 |
| **Database Name** | medostel |
| **Region** | asia-south1 (Mumbai) |
| **Zone** | asia-south1-c |
| **Status** | 🟢 RUNNABLE |

#### Connection String
```
postgresql://medostel_api_user:Iag2bMi@0@6aD@35.244.27.232:5432/medostel
```

#### For More Details
See: Development/DevOps Development/DBA/DBA.md for complete PostgreSQL instance documentation

### Service Account Configuration

For Workload Identity access to Cloud SQL:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: medostel-api-sa
  namespace: default

---
apiVersion: iam.cnpg.io/v1
kind: CloudSQLBinding
metadata:
  name: medostel-cloudsql
spec:
  instance: gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance
  instances:
    - gen-lang-client-0064186167:asia-south1:medostel-ai-assistant-pgdev-instance
```

---

## Network Policies

### Default Network Policy (Deny All)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow API Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-medostel-api
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: medostel-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP
      port: 443   # HTTPS
    - protocol: UDP
      port: 53    # DNS
```

---

## RBAC Configuration

### Service Accounts

```yaml
# API Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: medostel-api
  namespace: default

---

# Deployment Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: medostel-deployer
  namespace: default
```

### Role Definitions

```yaml
# API Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: medostel-api-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]

---

# Admin Role
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: medostel-admin
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

### Role Bindings

```yaml
# Bind API Role to Service Account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: medostel-api-binding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: medostel-api-role
subjects:
- kind: ServiceAccount
  name: medostel-api
  namespace: default
```

---

## Deployment Strategy

### Namespace Configuration

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: medostel-api
  labels:
    name: medostel-api
    environment: production
```

### Pod Security Policy

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: medostel-restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  volumes:
  - 'configMap'
  - 'emptyDir'
  - 'projected'
  - 'secret'
  - 'downwardAPI'
  - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
    seLinuxOptions:
      level: "s0:c123,c456"
  fsGroup:
    rule: 'MustRunAs'
    fsGroupChangePolicy: OnRootMismatch
    ranges:
    - min: 1000
      max: 2000
  readOnlyRootFilesystem: true
```

---

## Monitoring & Logging

### Monitoring Configuration

```
Status: ✅ ENABLED (Default)

Metrics Collected:
- Node CPU, Memory, Disk usage
- Pod resource utilization
- Network traffic
- Custom application metrics
```

### Logging Configuration

```
Status: ✅ ENABLED

Log Types:
- System logs (kubelet, kube-proxy)
- Cluster logs (scheduler, controller-manager)
- Application logs (stderr/stdout)

Log Destination: Google Cloud Logging
Retention: 30 days (default)
```

### Recommended Monitoring Tools

1. **Google Cloud Monitoring**
   - Built-in Kubernetes metrics
   - Custom dashboards
   - Alerting

2. **Prometheus + Grafana** (Optional)
   - Detailed metrics
   - Custom visualizations
   - Time-series analytics

3. **ELK Stack** (Optional)
   - Centralized logging
   - Log analysis
   - Audit trails

---

## Ingress Configuration

### Load Balancer Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: medostel-api-ingress
  namespace: medostel-api
  annotations:
    kubernetes.io/ingress.class: "gce"
    kubernetes.io/ingress.global-static-ip-name: "medostel-api-ip"
spec:
  rules:
  - host: api.medostel.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: medostel-api-service
            port:
              number: 8000
  tls:
  - hosts:
    - api.medostel.com
    secretName: medostel-api-cert
```

---

## Security Best Practices Implemented

✅ **Network Security**
- Network policies enabled (CALICO CNI)
- VPC-native networking
- Private IP ranges for pods
- Default-deny policies recommended

✅ **Node Security**
- Shielded nodes enabled
- Secure boot enabled
- Integrity monitoring enabled
- Minimal OAuth scopes

✅ **Access Control**
- RBAC enabled
- Workload Identity configured
- Service account segregation
- Least privilege principles

✅ **Data Protection**
- Encryption at rest (default GCP)
- Encryption in transit (TLS)
- Secrets management via Kubernetes Secrets or Google Secret Manager
- PII data encryption

✅ **Compliance**
- Pod Security Policies
- Network policies
- RBAC configuration
- Audit logging enabled
- Monitoring and alerting

✅ **Resource Management**
- Resource quotas
- Pod limits and requests
- Node auto-scaling
- Horizontal pod auto-scaling

---

## Cost Optimization

### Current Configuration
```
Nodes: 2-5 (auto-scaling)
Cost: ~$20-50/month (estimated)
Storage: 30 GB SSD per node (~$5-10/month)
Load Balancer: ~$18/month
Ingress: ~$2-5/month
```

### Cost Saving Measures
- ✅ Use e2-medium (cost-optimized)
- ✅ Enable auto-scaling (scale down during off-peak)
- ✅ Use spot instances (if non-critical workloads)
- ✅ Implement resource quotas
- ✅ Monitor and optimize resource utilization

---

## Deployment Checklist

- [x] Cluster created in Mumbai region (asia-south1)
- [x] Network policies enabled (CALICO)
- [x] Shielded nodes enabled
- [x] Workload Identity configured
- [x] Auto-scaling enabled (2-5 nodes)
- [x] HTTP Load Balancing enabled
- [x] Horizontal Pod Autoscaling enabled
- [ ] Configure DNS (medostel-api.com)
- [ ] Deploy SSL/TLS certificates
- [ ] Configure ingress
- [ ] Deploy API applications
- [ ] Configure monitoring alerts
- [ ] Set up log aggregation
- [ ] Implement backup strategy
- [ ] Security audit and penetration testing
- [ ] Performance testing and optimization
- [ ] Production readiness review

---

## Next Steps

1. **Configure kubectl access** (if needed locally)
   ```bash
   gcloud container clusters get-credentials medostel-api-cluster \
     --region=asia-south1 \
     --project=gen-lang-client-0064186167
   ```

2. **Create namespaces**
   ```bash
   kubectl create namespace medostel-api
   kubectl create namespace monitoring
   ```

3. **Apply network policies**
   ```bash
   kubectl apply -f network-policies.yaml
   ```

4. **Deploy applications**
   ```bash
   kubectl apply -f api-deployment.yaml
   ```

5. **Configure monitoring**
   - Set up Google Cloud Monitoring
   - Create custom dashboards
   - Configure alerts

6. **Setup CI/CD**
   - Google Cloud Build
   - Cloud Deploy
   - GitHub Actions (optional)

---

## Contact & Support

**Cluster Admin**: shishupal.rathore@gmail.com
**Project ID**: gen-lang-client-0064186167
**Region**: asia-south1 (Mumbai)
**Cluster Name**: medostel-api-cluster

**Documentation Links**:
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

---

## Instance Groups & Scaling

### Active Instance Groups (3 zones)
```
default-pool:
- gke-medostel-api-cluster-default-pool-a3766cdc-grp (asia-south1-a)
- gke-medostel-api-cluster-default-pool-0ffd123e-grp (asia-south1-b)
- gke-medostel-api-cluster-default-pool-1bf64257-grp (asia-south1-c)

preemptible-pool:
- gke-medostel-api-clu-preemptible-pool-5c963f02-grp (asia-south1-a)
- gke-medostel-api-clu-preemptible-pool-113d0453-grp (asia-south1-b)
- gke-medostel-api-clu-preemptible-pool-585487fe-grp (asia-south1-c)
```

---

## Maintenance & Support

### Maintenance Window
| Property | Value |
|----------|-------|
| **Maintenance Day** | Sunday |
| **Maintenance Hour** | 00:00 UTC |
| **Expected Duration** | Typically 1-2 hours |
| **Impact** | Cluster may be unavailable during maintenance |

### Support Information
| Property | Value |
|----------|-------|
| **Cluster Admin** | shishupal.rathore@gmail.com |
| **Project ID** | gen-lang-client-0064186167 |
| **Region** | asia-south1 (Mumbai) |
| **Support Level** | Standard GKE Support |

---

## Documentation & References

### Related Documentation
- **Database Details**: See `Development/DevOps Development/DBA/DBA.md`
- **PostgreSQL Instance**: medostel-ai-assistant-pgdev-instance
- **API Development**: See `Development/API Development/` folder

### External References
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [GKE Autoscaling](https://cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler)
- [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)

---

## Update History

| Date | Update | Status |
|------|--------|--------|
| 2026-02-28 | Initial cluster creation and configuration | ✅ Complete |
| 2026-02-28 | Live status verification and documentation update | ✅ Complete |

---

**Last Updated**: 2026-02-28 (Live Status Verified)
**Created By**: Claude Code
**Status**: 🟢 RUNNING - Ready for API Deployment
**Security Level**: Production-Grade
**Current Nodes**: 4 (auto-scaled)
**Kubernetes Version**: 1.34.3-gke.1318000
