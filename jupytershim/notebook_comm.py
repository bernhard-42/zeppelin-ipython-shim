from uuid import uuid4
from websocket import WebSocket
import json
import time

WSJS_TMPL = """
<script>
if(window._jupyter_comms == null) {
    window._jupyter_comms = {"comm": null, "notebookIds": []};
}

var notebook_id = "%s";
var wsServer = "%s";

if(!window._jupyter_comms.notebookIds.includes(notebook_id)) {
    Jupyter = {}
    Jupyter.notebook = new Notebook(Jupyter, notebook_id, wsServer);
    window._jupyter_comms.notebookIds.push(notebook_id);
}
</script>
"""

class ZeppelinNotebookComm():
    
    def __init__(self, wsServer, jupyterShim):
        self.notebookId = str(uuid4())
        self.jupyterShim = jupyterShim
        self.ws = WebSocket()
        self.ws.connect(wsServer)
        self.send("init", "initialize")
        time.sleep(0.1)
        
        self.jupyterShim._print(WSJS_TMPL % (self.notebookId, wsServer), True)
    
    def send(self, task, msg):
        self.ws.send(json.dumps({"notebook_id":self.notebookId, "task":task, "node":"interpreter", "msg":msg}))
        
    def receive(self):
        return self.ws.recv()

