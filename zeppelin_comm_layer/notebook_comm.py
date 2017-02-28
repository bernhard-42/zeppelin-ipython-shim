from uuid import uuid4
import json
import time

WSJS_TMPL = """
<script>
    var execution_id = "%s";                                                 // Zeppelin 0.7.0 double print workaround
    if(window.__zeppelin_already_executed__ == null) {                       // Zeppelin 0.7.0 double print workaround
        window.__zeppelin_already_executed__ = [];                           // Zeppelin 0.7.0 double print workaround
    }                                                                        // Zeppelin 0.7.0 double print workaround
    if(!window.__zeppelin_already_executed__.includes(execution_id)) {       // Zeppelin 0.7.0 double print workaround
        var $scope = angular.element(document.getElementById("%s")).scope();

        if(typeof(window.__zeppelin_notebook_unwatchers__) !== "undefined") {
            console.info("NoteboooComm: cancel watchers");
            var unwatchers = window.__zeppelin_notebook_unwatchers__
            for(i in unwatchers) {
                unwatchers[i]();
            }
        }

        if((typeof(Jupyter) === "undefined") || (Jupyter === null)) {
            console.info("Initiate Javascript Notebook Comms");
            Jupyter = {};
            Jupyter.notebook = new Notebook(Jupyter);
        }

        window.__zeppelin_notebook_unwatchers__ = [];
        var unwatch = $scope.$watch("__zeppelin_comm_msg__", function(newValue, oldValue, scope) {
            if(typeof(newValue) !== "undefined") {
                // console.info("__zeppelin_comm_msg__: " + JSON.stringify(newValue));
                Jupyter.notebook.kernel.notebookComm.handleMsg(newValue);
            }
        }, true)

        window.__zeppelin_notebook_unwatchers__.push(unwatch)

        window.__zeppelin_already_executed__.push(execution_id);             // Zeppelin 0.7.0 double print workaround
    } else {
        console.info("zeppelin bug, angular script already executed, skipped");
    }
</script>
"""

class ZeppelinNotebookComm:

    def __init__(self, zeppelinCommLayer, zeppelinContext, debug=False):
        self.id = 0
        self.z = zeppelinContext
        self.debug = debug
        self.zeppelinCommLayer = zeppelinCommLayer
        self.notebookCommDivId = "__Zeppelin_Notebook_Comm__"
        self.reset()

        # div must exist before javascript below can be printed
        self.z.angularBind("__zeppelin_comm_status__", "")
        print("""%%angular <div id="%s">{{__zeppelin_comm_status__}}</div>\n""" % self.notebookCommDivId)

    def start(self):
        if self.debug:
            print("""%angular Debug: {{__zeppelin_comm_msg__}}""")

        print("%angular") 
        print(WSJS_TMPL % (str(uuid4()), self.notebookCommDivId))
        self.z.angularBind("__zeppelin_comm_status__", "ZeppelinCommLayer initialized (do not delete this paragraph)")
        
    def send(self, task, msg):
        self.id += 1
        self.z.angularBind("__zeppelin_comm_msg__", {"task":task, "msg":msg})
        
    def reset(self):
        self.z.angularUnbind("__zeppelin_comm_msg__")
        self.id = 0