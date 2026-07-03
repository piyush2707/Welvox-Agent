# WelvoxAgent Deployment Guide

## Deployment Options

WelvoxAgent can be deployed on various platforms:

1. **Docker Compose** (Development/Small scale)
2. **Kubernetes** (Production/Enterprise)
3. **Cloud Platforms** (AWS, GCP, Azure)
4. **Serverless** (AWS Lambda, Google Cloud Functions)

---

## Prerequisites

- Docker & Docker Compose (all environments)
- kubectl (for Kubernetes)
- Cloud provider CLI (AWS CLI, gcloud, etc.)
- SSL certificate for HTTPS
- Domain name configured

---

## Docker Compose Deployment (Local/Small Scale)

### 1. Configure Environment
```bash
cp .env.example .env
```

Update `.env` with production values:
```env
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://welvox:secure_password@postgres:5432/welvox_db

# Redis
REDIS_URL=redis://redis:6379/0

# API Keys
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIz...

# Clerk Auth
CLERK_SECRET_KEY=sk_live_...
CLERK_PUBLISHABLE_KEY=pk_live_...

# Security
JWT_SECRET=$(openssl rand -base64 32)
ENCRYPTION_KEY=$(openssl rand -base64 32)

# URLs
NEXT_PUBLIC_API_URL=https://api.welvox.ai
NEXT_PUBLIC_WS_URL=wss://api.welvox.ai/ws
```

### 2. Build Images
```bash
docker-compose build
```

### 3. Start Services
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Initialize Database
```bash
docker-compose exec api python -m alembic upgrade head
docker-compose exec api python -m scripts.seed_db
```

### 5. Verify Deployment
```bash
# Health check
curl https://api.welvox.ai/health

# Check containers
docker-compose ps

# View logs
docker-compose logs api
```

---

## Kubernetes Deployment (Production)

### 1. Prerequisites

Install tools:
```bash
kubectl version --client
helm version
```

### 2. Create Kubernetes Cluster

**AWS EKS:**
```bash
eksctl create cluster \
  --name welvox-production \
  --region us-east-1 \
  --nodegroup-name main \
  --node-type t3.large \
  --nodes 3
```

**GCP GKE:**
```bash
gcloud container clusters create welvox-production \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2
```

**Azure AKS:**
```bash
az aks create \
  --resource-group welvox \
  --name welvox-production \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets
```

### 3. Create Kubernetes Manifests

**Namespace:**
```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: welvox
```

**ConfigMap (Environment):**
```yaml
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: welvox-config
  namespace: welvox
data:
  ENVIRONMENT: production
  LOG_LEVEL: INFO
  NEXT_PUBLIC_API_URL: https://api.welvox.ai
```

**Secret (Credentials):**
```bash
# Create secret from .env
kubectl create secret generic welvox-secrets \
  --from-env-file=.env \
  --namespace=welvox

# Or create manually
kubectl create secret generic welvox-secrets \
  --from-literal=ANTHROPIC_API_KEY=sk-... \
  --from-literal=DATABASE_URL=postgres://... \
  --namespace=welvox
```

**PostgreSQL StatefulSet:**
```yaml
# kubernetes/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: welvox
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: welvox_db
        - name: POSTGRES_USER
          value: welvox
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: welvox-secrets
              key: DB_PASSWORD
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
```

**Redis Deployment:**
```yaml
# kubernetes/redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: welvox
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**FastAPI Deployment:**
```yaml
# kubernetes/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: welvox
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: docker.io/YOUR_REGISTRY/welvox-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: welvox-config
        - secretRef:
            name: welvox-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
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
                  - api
              topologyKey: kubernetes.io/hostname
```

**Next.js Deployment:**
```yaml
# kubernetes/web-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: welvox
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: docker.io/YOUR_REGISTRY/welvox-web:latest
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: welvox-config
        - secretRef:
            name: welvox-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Services:**
```yaml
# kubernetes/services.yaml
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: welvox
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
  - port: 8000
    targetPort: 8000

---
apiVersion: v1
kind: Service
metadata:
  name: web
  namespace: welvox
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 3000
  - port: 443
    targetPort: 3000

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: welvox
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432

---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: welvox
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

### 4. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Create secrets
kubectl apply -f kubernetes/secrets.yaml

# Deploy all services
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods -n welvox
kubectl get svc -n welvox
kubectl logs -n welvox deployment/api
```

### 5. Setup Ingress for HTTPS

```yaml
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: welvox-ingress
  namespace: welvox
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - welvox.ai
    - api.welvox.ai
    secretName: welvox-tls
  rules:
  - host: welvox.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 3000
  - host: api.welvox.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 8000
```

---

## AWS Deployment (ECS)

### 1. Create Task Definitions

```json
{
  "family": "welvox-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/welvox-api:latest",
      "portMappings": [
        {
          "containerPort": 8000
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:...:secret:..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/welvox-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 2. Create ECS Service

```bash
aws ecs create-service \
  --cluster welvox \
  --service-name api \
  --task-definition welvox-api:1 \
  --desired-count 3 \
  --load-balancers targetGroupArn=arn:aws:...,containerName=api,containerPort=8000
```

---

## Database Backups

### Automated Backups

**AWS RDS:**
```bash
aws rds create-db-snapshot \
  --db-instance-identifier welvox-db \
  --db-snapshot-identifier welvox-db-backup-$(date +%Y%m%d)
```

**PostgreSQL Backup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

pg_dump postgresql://welvox:password@localhost/welvox_db \
  | gzip > $BACKUP_DIR/welvox_$TIMESTAMP.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/welvox_$TIMESTAMP.sql.gz s3://welvox-backups/
```

---

## Monitoring & Logging

### CloudWatch (AWS)
```bash
# Create log group
aws logs create-log-group --log-group-name /welvox/api

# View logs
aws logs tail /welvox/api --follow
```

### DataDog
```yaml
# kubernetes/datadog.yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-secret
  namespace: welvox
type: Opaque
stringData:
  api-key: YOUR_DD_API_KEY
  app-key: YOUR_DD_APP_KEY
```

---

## SSL/TLS Setup

### Using cert-manager (Kubernetes)

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@welvox.ai
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

---

## Health Checks

```bash
# API health
curl https://api.welvox.ai/health

# Database connection
curl https://api.welvox.ai/health/db

# Redis connection
curl https://api.welvox.ai/health/redis
```

---

## Rollback Procedure

### Docker Compose
```bash
# Rollback to previous image
docker-compose down
git checkout previous-commit
docker-compose up -d
```

### Kubernetes
```bash
# Check rollout history
kubectl rollout history deployment/api -n welvox

# Rollback to previous version
kubectl rollout undo deployment/api -n welvox

# Rollback to specific revision
kubectl rollout undo deployment/api --to-revision=3 -n welvox
```

---

## Scaling

### Kubernetes Auto-scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-autoscaler
  namespace: welvox
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 10
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
```

---

## Monitoring Checklist

- [ ] Set up log aggregation
- [ ] Configure alerts for errors
- [ ] Monitor API response times
- [ ] Track database performance
- [ ] Monitor memory/CPU usage
- [ ] Setup uptime monitoring
- [ ] Configure error tracking (Sentry)
- [ ] Track cost metrics

---

## Support

For deployment issues:
- Email: deploy@welvox.ai
- Slack: #deployment-support
- Docs: https://docs.welvox.ai/deployment

