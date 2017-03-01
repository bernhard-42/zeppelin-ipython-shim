    # Copyright 2017 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from uuid import uuid4
import json
import time
from .logger import Logger


WSJS_TMPL = """
<script>
    var sessionCommVar = "%s";
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

        console.info("Initiate Javascript Notebook Comms");
        Jupyter = {};
        Jupyter.notebook = new Notebook(Jupyter);

        window.__zeppelin_notebook_unwatchers__ = [];
        var unwatch = $scope.$watch(sessionCommVar, function(newValue, oldValue, scope) {
            if(typeof(newValue) !== "undefined") {
                // console.info(sessionCommVar + ": " + JSON.stringify(newValue));
                Jupyter.notebook.kernel.session.handleMsg(newValue);
            }
        }, true)

        window.__zeppelin_notebook_unwatchers__.push(unwatch)

        window.__zeppelin_already_executed__.push(execution_id);             // Zeppelin 0.7.0 double print workaround
    } else {
        console.info("Angular script already executed, skipped");
    }
</script>
"""

class ZeppelinSession:

    def __init__(self, zeppelinCommLayer, zeppelinContext, debug=False):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.info("New ZeppelinSession")
           
        self.id = 0
        self.zeppelinContext = zeppelinContext
        self.debug = debug

        sessionCommDivId, sessionCommVar, sessionStatusVar = self.sessionVars(all=True)
        self.reset(sessionCommVar)

        # div must exist before javascript below can be printed
        self.zeppelinContext.angularBind(sessionStatusVar, "")
        print("""%%angular <div id="%s">{{%s}}</div>\n""" % (sessionCommDivId, sessionStatusVar))

    def start(self):
        sessionCommDivId, sessionCommVar, sessionStatusVar = self.sessionVars(all=True)
        self.logger.debug("Starting Angular watcher for $scope.%s" % sessionCommVar)
        if self.debug:
            print("""%%angular Debug: {{%s}}""" % sessionCommVar)

        print("%angular") 
        print(WSJS_TMPL % (sessionCommVar, str(uuid4()), sessionCommDivId))
        self.zeppelinContext.angularBind(sessionStatusVar, "ZeppelinCommLayer initialized (do not delete this paragraph)")
        
    def send(self, task, msg):
        sessionCommVar = self.sessionVars(all=False)
        self.logger.debug("Sending task %s to $scope.%s for message %s" % (task, sessionCommVar, msg))
        self.id += 1
        self.zeppelinContext.angularBind(sessionCommVar, {"task":task, "msg":msg})
        
    def reset(self, sessionCommVar):
        sessionCommVar = self.sessionVars(all=False)
        self.logger.debug("Reset $scope.%s" % sessionCommVar)
        self.zeppelinContext.angularUnbind(sessionCommVar)
        self.id = 0

    def sessionVars(self, all=True):
        noteId = self.zeppelinContext.getInterpreterContext().getNoteId()
        sessionCommVar = "____zeppelin_comm_%s_msg__" % noteId
        if all:
            sessionCommDivId = "__Zeppelin_Session_%s_Comm__" % noteId
            sessionStatusVar = "____zeppelin_comm_%s_status__" % noteId
            return (sessionCommDivId, sessionCommVar, sessionStatusVar)
        else:
            return sessionCommVar

