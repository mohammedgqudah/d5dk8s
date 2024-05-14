import os
from typing import AnyStr
import requests
from urllib.parse import urljoin

token = os.getenv('D5DK8S_BOT_TOKEN')
api_server: str = os.getenv('K8S_API_SERVER')


class APIServer(requests.Session):
    def __init__(self, base_url: AnyStr):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)

session = APIServer(base_url=api_server)

token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
ca_cert_path = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

try:
    with open(token_path, 'r') as f:
        token = f.read().strip()

    session.headers.update({
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })
    session.verify = ca_cert_path
except FileNotFoundError as e:
    # When running the bot locally through a proxy
    print("Couldn't find the service token");
