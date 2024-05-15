# D5DK8S
A discord bot to inspect a kubernetes cluster (an experiment)

> The motive behind this bot is to learn more about the kubernetes API server and service accounts.


## Testing - Locally
Start a proxy server
```
k proxy 8000 &
```
Start the bot
```
export K8S_API_SERVER='http://localhost:8001'
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
  D5DK8S_BOT_TOKEN: "secretBotToken"
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
          imagePullPolicy: IfNotPresent
          envFrom:
            - secretRef:
                name: d5dk8s-secret
          env:
            - name: K8S_API_SERVER
              value: "https://kubernetes.default.svc"
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
