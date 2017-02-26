from uuid import uuid4
from websocket import WebSocket
import json
import time

WSJS_TMPL = """
<script>
    var execution_id = "%s";                                                 // Zeppelin double print workaround
    if(window.__zeppelin_already_executed__ == null) {                       // Zeppelin double print workaround
        window.__zeppelin_already_executed__ = [];                           // Zeppelin double print workaround
    }                                                                        // Zeppelin double print workaround
    if(!window.__zeppelin_already_executed__.includes(execution_id)) {       // Zeppelin double print workaround

        var $scope = angular.element(document.getElementById("%s")).scope();

        if(typeof(window.__jupyter_notebook_unwatchers__) !== "undefined") {
            console.info("NoteboooComm: cancel watchers");
            var unwatchers = window.__jupyter_notebook_unwatchers__
            for(i in unwatchers) {
                unwatchers[i]();
            }
        }

        if((typeof(Jupyter) === "undefined") || (Jupyter === null)) {
            console.info("Initiate Javascript Notebook Comms");
            Jupyter = {};
            Jupyter.notebook = new Notebook(Jupyter);
        }

        window.__jupyter_notebook_unwatchers__ = [];
        
        var unwatch = $scope.$watch("__jupyter_comm_msg__", function(newValue, oldValue, scope) {
            if(typeof(newValue) !== "undefined") {
                // console.info("__jupyter_comm_msg__: " + JSON.stringify(newValue));
                Jupyter.notebook.kernel.notebookComm.handleMsg(newValue);
            }
        }, true)
        window.__jupyter_notebook_unwatchers__.push(unwatch)

        window.__zeppelin_already_executed__.push(execution_id);             // Zeppelin double print workaround
    } else {
        console.info("zeppelin bug, angular script already executed, skipped");
    }
</script>
"""

class ZeppelinNotebookComm:

    def __init__(self, jupyterShim, zeppelinContext, debug=False):
        self.id = 0
        self.z = zeppelinContext
        self.jupyterShim = jupyterShim
        self.notebookCommDivId = "__Jupyter_Notebook_Comm__"
        self.reset()
        
        # div must exist before javascript below can be printed
        print("""%%angular <div id="%s">Shim initialized (do not delete this paragraph)</div>""" % self.notebookCommDivId)
        
        if debug:
            print("""%angular Debug: {{__jupyter_comm_msg__}}""")
            
        print("%angular") 
        print(WSJS_TMPL % (str(uuid4()), self.notebookCommDivId))
        
    def send(self, task, msg):
        self.id += 1
        self.z.angularBind("__jupyter_comm_msg__", {"task":task, "msg":msg})
        
    def reset(self):
        self.z.angularUnbind("__jupyter_comm_msg__")
        self.id = 0
