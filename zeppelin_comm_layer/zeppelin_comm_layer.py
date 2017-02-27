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
from os.path import dirname 
from .notebook_comm import ZeppelinNotebookComm
from .display_pub import ZeppelinDisplayPublisher
from .comm import ZeppelinComm
from .comm_manager import ZeppelinCommManager
from .kernel import Kernel


class ZeppelinCommLayer:

    class _ZeppelinCommLayer:
    
        def __init__(self, zeppelinContext, debug=False):
            self.zeppelinContext = zeppelinContext
            self.debug = debug
            self._loadJsLibs()
            
            from IPython.core.interactiveshell import InteractiveShell
            self.ip = InteractiveShell.instance()
            
            session = ZeppelinNotebookComm(self, self.zeppelinContext, self.debug)
            commManager = ZeppelinCommManager()
            kernel = Kernel(commManager, session)
            self.ip.kernel = kernel

            import ipykernel.comm
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager

            self.ip.display_pub = ZeppelinDisplayPublisher(self)

        def start(self):
            self.ip.kernel.session.start()
            
        def _loadJsLibs(self):
            jsScript = open("%s/js/zeppelin_comm_layer-min.js" % dirname(__file__), "r").read() + "\n"
            self._printJs(jsScript, header=True, delayed=False)
            
        def _print(self, html, header=False, delayed=True):
            if header:
                print("%angular")
            if delayed:
                div_id = str(uuid4())
                wrapper = '<div id="%s"></div>' % div_id
                print(wrapper)
                self.ip.kernel.session.send("publish", {"div_id":div_id, "html":html})
            else:
                print(html)
        
        def _printJs(self, script, header=False, delayed=True):
            wrapper = '<script type="text/javascript">' + script + '</script>'
            self._print(wrapper, header, delayed)

    instance = None

    def __init__(self, zeppelinContext=None, debug=False):
        if not ZeppelinCommLayer.instance:
            ZeppelinCommLayer.instance = ZeppelinCommLayer._ZeppelinCommLayer(zeppelinContext, debug)
            
    def __getattr__(self, name):
        return getattr(self.instance, name)


def resetZeppelinCommLayer(zeppelinContext):
    ZeppelinCommLayer.instance = None
    zeppelinContext.angularBind("__zeppelin_comm_msg__", "")
    zeppelinContext.angularUnbind("__zeppelin_comm_msg__")
    print("%angular <script>Jupyter=null;</script>")