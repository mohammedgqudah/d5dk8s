from typing import Any
import yaml
import os

class Config:
    _config = {}

    @classmethod
    def load_config(cls, file_path):
        with open(file_path, 'r') as file:
            cls._config = yaml.safe_load(file)

    @classmethod
    def get(cls, key, default=None) -> Any:
        """Gets a config value from environment variables or YML config.
        
        example: D5DK8S_CONFIG_PROMETHEUS_URL=prometheus.default.svc.cluster.local
        """
        # check if the value is set in the environment variables first
        env_value = os.getenv('D5DK8S_CONFIG_' + key.replace('.', '_').upper())
        if env_value is not None:
            return env_value

        # if the value was not found in environment variables, look
        # in the YML config.
        keys = key.split('.')
        value = cls._config
        for k in keys:
            value = value.get(k, default)
            if value is default:
                break
        return value
