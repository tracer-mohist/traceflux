# Python code sample for testing traceflux

import os
import requests

def setup_proxy(config):
    """Setup proxy from config."""
    proxy = os.getenv('HTTP_PROXY')
    if not proxy:
        proxy = config.get('proxy_url')
    
    session = requests.Session()
    session.proxies = {
        'http': proxy,
        'https': proxy
    }
    return session

def load_config():
    """Load configuration."""
    return {
        'proxy_url': 'http://proxy.example.com:8080',
        'timeout': 30
    }

if __name__ == '__main__':
    config = load_config()
    session = setup_proxy(config)
