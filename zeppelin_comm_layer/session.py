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


#  Session Messages:
#
#  Basic
#  - register    register a javascript function
#  - unregister  unregister a javascript function
#  - call        call a registered javascript function 
#  - dump        log $scope to Web Coinsole for debugging
# 
# Jupyter communications
#  - comm_open   Open a Juppyter communication channel
#  - comm_close  Close a Juppyter communication channel
#  - comm_msg    Send a message across a Juppyter communication channel
#  - comm_reset  Reset a Juppyter communication channel


def _JAVASCRIPT(sessionCommVar, sessionCommDivId):
    execution_id = str(uuid4())
    jsScript = """
<script>
    var sessionCommVar = "%s";
    var sessionCommDivId = "%s"
    var execution_id = "%s";                                                 // Avoid double execution
    if(window.__zeppelin_already_executed__ == null) {                       //
        window.__zeppelin_already_executed__ = [];                           //
    }                                                                        //
    if(!window.__zeppelin_already_executed__.includes(execution_id)) {       // Avoid double execution

        // Get the angular scope of the session div element

        console.log("Get scope for div id" + sessionCommDivId);
        var $scope = angular.element(document.getElementById(sessionCommDivId)).scope();

        // make scope easily accessible in Web Console

        window.__zeppelin_comm_scope = $scope;

        // Remove any remaining watcher from last session

        if(typeof(window.__zeppelin_notebook_unwatchers__) !== "undefined") {
            console.info("NoteboooComm: Cancel watchers");
            var unwatchers = window.__zeppelin_notebook_unwatchers__
            for(i in unwatchers) {
                unwatchers[i]();
            }
        }
        
        // Array to note all active watchers (as with their respective unwatcher function)

        window.__zeppelin_notebook_unwatchers__ = [];

        // Initiate Jupyter communication system

        console.info("Initiate Javascript Notebook Comms for divId " + sessionCommDivId);
        Jupyter = {};
        Jupyter.notebook = new Notebook(Jupyter);

        // Main Handler

        console.info("Install Angular watcher for session comm var " + sessionCommVar);
        var unwatch = $scope.$watch(sessionCommVar, function(newValue, oldValue, scope) {
            if(typeof(newValue) !== "undefined") {
 
                if (newValue.task === "call") {

                    // Format: newValue = {"id": int, task":"call", "msg":{"function":"func_name", "object":"json_string"}}
                    
                    var data = newValue.msg;
                    if (typeof($scope.__functions[data.function]) === "function") {
                        $scope.__functions[data.function]($scope, data.object);
                    } else {
                        console.error("Unknown function: " + data.function + "()")
                    }
                    
                } else if (newValue.task === "register") {
                    
                    // Format: newValue = {"id": int, task":"register", "msg":{"function":"func_name", "funcBody":"function_as_string"}}
                    
                    var data = newValue.msg;
                    var func = eval(data.funcBody);
                    $scope.__functions[data.function] = func;
                    
                } else if (newValue.task === "unregister") {
                    
                    // Format: newValue = {"id": int, task":"unregister", "msg":{"function":"func_name"}}
                    
                    var data = newValue.msg;
                    if (typeof($scope.__functions[data.function]) === "function") {
                        delete $scope.__functions[data.function];
                    }               
                    
                } else if (newValue.task === "dump") {
                    
                    // Format: newValue = {"id": int, task":"dump", "msg":{}}
                    
                    console.log("sessionCommDivId: ", sessionCommDivId);
                    console.log("$scope: ", $scope);

                } else {

                    // Maybe it is a Jupyter notebook session?

                    Jupyter.notebook.kernel.session.handleMsg(newValue);
                }
            }
        }, true)

        // Initialize the object that will hold the registered functions
        $scope.__functions = {};
        
        // remember unwatch function to clean up later
        window.__zeppelin_notebook_unwatchers__.push(unwatch)

        // mark init as executed
        window.__zeppelin_already_executed__.push(execution_id);            // Avoid double execution
    } else {                                                                //
        console.info("Angular script already executed, skipped");           //
    }                                                                       // Avoid double execution
</script>
""" % (sessionCommVar, sessionCommDivId, execution_id)
    return jsScript


class ZeppelinSession:

    def __init__(self, zeppelinContext, jsScript=None):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.propagate = False
        self.logger.info("New ZeppelinSession")

        self.id = 0
        self.zeppelinContext = zeppelinContext
        self.jsScript = jsScript


    #
    # Initialization methods.
    # 
    # init:  creates div
    # start: starts the communication system relying on the existence of the div (hence seaprate Zeppelin paragraph)
    #

    def init(self):
        self.logger.debug("Initializing ZeppelinSession")
        sessionCommDivId, sessionCommVar, sessionStatusVar = self._sessionVars(all=True)
        self.logger.debug("Reset $scope.%s" % sessionCommVar)
        self.zeppelinContext.angularUnbind(sessionCommVar)
        self.zeppelinContext.angularUnbind(sessionStatusVar)

        # div must exist before javascript below can be printed
        print("%angular")
        if self.jsScript:
            print("""<script>{{%s}}</script>\n""" % self.jsScript)
        print("""<div id="%s">{{%s}}</div>\n""" % (sessionCommDivId, sessionStatusVar))
        self.zeppelinContext.angularBind(sessionStatusVar, "Session initialized, can now be started in the next paragraph ...  (do not delete this paragraph)")

    def start(self, notebook_comm=True):
        self.logger.debug("Starting ZeppelinSession")
        sessionCommDivId, sessionCommVar, sessionStatusVar = self._sessionVars(all=True)

        self.zeppelinContext.angularBind(sessionStatusVar, "ZeppelinSession started (do not delete this paragraph)")
        print("%angular") 
        print(_JAVASCRIPT(sessionCommVar, sessionCommDivId))
    
    #
    # Helper methods
    #

    def _sessionVars(self, all=True):
        noteId = self.zeppelinContext.getInterpreterContext().getNoteId()
        sessionCommVar = "____zeppelin_comm_%s_msg__" % noteId
        if all:
            sessionCommDivId = "__Zeppelin_Session_%s_Comm__" % noteId
            sessionStatusVar = "____zeppelin_comm_%s_status__" % noteId
            return (sessionCommDivId, sessionCommVar, sessionStatusVar)
        else:
            return sessionCommVar

    def _dumpScope(self):
        self.send("dump", {})

    def _reset(self):
        self.logger.debug("Ressetting ZeppelinSession")
        sessionCommDivId, sessionCommVar, sessionStatusVar = self._sessionVars(all=True)
        self.zeppelinContext.angularBind(sessionCommVar, {"task":"comm_reset", "msg":{}})
        time.sleep(0.2)
        self.zeppelinContext.angularUnbind(sessionCommVar)
        self.zeppelinContext.angularUnbind(sessionStatusVar)

    #
    # Basic communication and display methods
    #

    def send(self, task, msg):
        sessionCommVar = self._sessionVars(all=False)
        self.logger.debug("Sending task %s to $scope.%s for message %s" % (task, sessionCommVar, msg))
        self.id += 1
        self.zeppelinContext.angularBind(sessionCommVar, {"id": self.id, "task":task, "msg":msg})

    def print(self, html, header=False):
        if header:
            print("%angular")
        div_id = str(uuid4())
        wrapper = '<div id="%s"></div>' % div_id
        print(wrapper)
        self.logger.debug("Delayed printing of " + wrapper)
        self.send("publish", {"div_id":div_id, "html":html})
    
    def printJs(self, script, header=False):
        wrapper = '<script>' + script + '</script>'
        self.print(wrapper, header)

    #
    # Angular Variable handling
    #

    def setVar(self, var, value):
        self.logger.debug("Set var %s" % var)
        self.zeppelinContext.angularBind(var, value)
        
    def getVar(self, var, delay=0.2):
        self.logger.debug("Get var %s" % var)
        time.sleep(delay)
        return self.zeppelinContext.angular(var)
        
    def deleteVar(self, var):
        self.logger.debug("Delete var %s" % var)        
        self.zeppelinContext.angularUnbind(var)
        
    #
    # Angular Functions handling
    #

    def registerFunction(self, funcName, jsFunc):
        self.logger.debug("Register function %s with: %s" % (funcName, jsFunc))        
        self.send("register", {"function": funcName, "funcBody": jsFunc})
    
    def unregisterFunction(self, funcName):
        self.logger.debug("Unregister function %s" % funcName)
        self.send("unregister", {"function": funcName})

    def call(self, funcName, object):
        self.logger.debug("Call function %s" % funcName)
        self.send("call", {"function": funcName, "object": object})
        
