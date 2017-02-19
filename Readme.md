### Usage

## Terminal

```bash
cd websocket-server/
python3 websocketServer.py
```

## Zeppelin

```python
import sys
sys.path += ["/path/to/this/folder"]

from jupytershim import JupyterShim
  
wsServer = "ws://<ws-server>:<port>"
j = JupyterShim(wsServer)
```