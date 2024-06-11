# kube-inspector-bot
A discord bot to inspect a kubernetes cluster (an experiment)

> The motive behind this bot is to learn more about the kubernetes API server and service accounts.

## Deploying - Kubernetes
[Deployment Example](examples)

## Testing - Locally
Start a proxy server
```bash
kubectl proxy 8000 --accept-hosts='^localhost$,^127\.0\.0\.1$,^\[::1\]$,^host.docker.internal$' &
# if using prometheus
kubectl port-forward svc/prometheus 8002:80 &
```

Start the bot
```bash
cp .env.example .env
docker compose up
```
