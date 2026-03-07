# Test Project

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set up proxy:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=https://proxy.example.com:8080
```

## Usage

```python
from myapp import setup_proxy, load_config

config = load_config()
session = setup_proxy(config)
```

## Troubleshooting

If you see connection timeout errors:
1. Check proxy settings
2. Verify network connectivity
3. Try without proxy
