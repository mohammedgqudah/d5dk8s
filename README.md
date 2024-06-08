# D5DK8S
A discord bot to inspect a kubernetes cluster (an experiment)

> The motive behind this bot is to learn more about the kubernetes API server and service accounts.


## Testing - Locally
Start a proxy server
```bash
kubectl proxy 8000 --accept-hosts='^localhost$,^127\.0\.0\.1$,^\[::1\]$,^host.docker.internal$' &
# if using prometheus
kubectl port-forward svc/prometheus 8002:80 &
```

Start the bot
```bash
export D5DK8S_CONFIG_API_SERVER='http://localhost:8001'
python -m d5dk8s
```

## Deploying - Kubernetes
```yml
# secret.yml

apiVersion: v1
kind: Secret
metadata:
  name: d5dk8s-secret
stringData:
  D5DK8S_CONFIG_BOT_TOKEN: "secretBotToken"
```

```yml
# deployment.yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: d5dk8s
spec:
  selector:
    matchLabels:
      app: d5dk8s
  template:
    metadata:
      labels:
        app: d5dk8s
    spec:
      serviceAccountName: d5dk8s
      containers:
        - name: d5dk8s
          image: ghcr.io/mohammedgqudah/d5dk8s:latest  
          args:
            - "--config=/etc/d5dk8s/d5dk8s.yml"
          imagePullPolicy: IfNotPresent
          envFrom:
            - secretRef:
                name: d5dk8s-secret
          env:
            - name: D5DK8S_CONFIG_API_SERVER
              value: "https://kubernetes.default.svc"
          volumeMounts:
            - name: d5dk8s-config
              mountPath: /etc/d5dk8s
      volumes:
        - name: d5dk8s-config
          configMap:
            name: d5dk8s-config
```

```yml
# account-service.yml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: d5dk8s
---
# cluster-role.yml

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: discoverer
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
---
# cluster-role-binding.yml

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: d5dk8s-discoverer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: discoverer
subjects:
- kind: ServiceAccount
  name: d5dk8s
  namespace: default
```


## Development

### Auto generating migrations
```
docker exec --tty -i d5dk8s-bot-1 alembic revision --autogenerate -m "MESSAGE"
```
