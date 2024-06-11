# kube-inspector-bot
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
export BOT_CONFIG_API_SERVER='http://localhost:8001'
python -m bot
```

## Deploying - Kubernetes
```yml
# secret.yml

apiVersion: v1
kind: Secret
metadata:
  name: kube-inspector-bot-secret
stringData:
  BOT_CONFIG_BOT_TOKEN: "secretBotToken"
```

```yml
# deployment.yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: kube-inspector-bot
spec:
  selector:
    matchLabels:
      app: kube-inspector-bot
  template:
    metadata:
      labels:
        app: kube-inspector-bot
    spec:
      serviceAccountName: kube-inspector-bot
      containers:
        - name: kube-inspector-bot
          image: ghcr.io/mohammedgqudah/kube-inspector-bot:latest  
          args:
            - "--config=/etc/kube-inspector-bot/bot.yml"
          imagePullPolicy: IfNotPresent
          envFrom:
            - secretRef:
                name: kube-inspector-bot-secret
          env:
            - name: BOT_CONFIG_API_SERVER
              value: "https://kubernetes.default.svc"
          volumeMounts:
            - name: kube-inspector-bot-config
              mountPath: /etc/kube-inspector-bot
      volumes:
        - name: kube-inspector-bot-config
          configMap:
            name: kube-inspector-bot-config
```

```yml
# account-service.yml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-inspector-bot
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
  name: kube-inspector-bot-discoverer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: discoverer
subjects:
- kind: ServiceAccount
  name: kube-inspector-bot
  namespace: default
```


## Development

### Auto generating migrations
```
docker exec --tty -i d5dk8s-bot-1 alembic revision --autogenerate -m "MESSAGE"
```
