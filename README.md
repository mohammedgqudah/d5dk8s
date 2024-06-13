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

## Screenshots
<p align="center">
<img width="780" alt="image" src="https://github.com/mohammedgqudah/kube-inspector-bot/assets/26502088/ec810497-a9ba-4578-8417-98f34d1b69a2">
</p>
<p align="center">
<img width="779" alt="image" src="https://github.com/mohammedgqudah/kube-inspector-bot/assets/26502088/e3bd4847-49ef-404a-992e-6c442f7ba3e4">

</p>
<p align="center">
<img width="780" alt="image" src="https://github.com/mohammedgqudah/kube-inspector-bot/assets/26502088/ff96ea5e-4604-4ba5-b801-61b4039f0bc3">
</p>
