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


class JupyterShim:

    class _JupyterShim:
    
        def __init__(self, zeppelinContext, debug=False):
            self.zeppelinContext = zeppelinContext
            
            from IPython.core.interactiveshell import InteractiveShell
            self.ip = InteractiveShell.instance()
            
            session = ZeppelinNotebookComm(self, zeppelinContext, debug)
            commManager = ZeppelinCommManager()
            kernel = Kernel(commManager, session)
            self.ip.kernel = kernel

            import ipykernel.comm
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager

            self._loadJsLibs()

            self.ip.display_pub = ZeppelinDisplayPublisher(self)

        def _loadJsLibs(self):
            jsScript = open("%s/js/jupytershim-min.js" % dirname(__file__), "r").read() + "\n"
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
        if not JupyterShim.instance:
            JupyterShim.instance = JupyterShim._JupyterShim(zeppelinContext, debug)
            
    def __getattr__(self, name):
        return getattr(self.instance, name)


def jupyterReset():
    print("%angular <script>Jupyter=null;</script>")
    JupyterShim.instance = None