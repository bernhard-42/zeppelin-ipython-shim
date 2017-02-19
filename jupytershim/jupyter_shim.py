from uuid import uuid4
from os.path import dirname 
from .notebook_comm import ZeppelinNotebookComm
from .display_pub import ZeppelinDisplayPublisher
from .comm import ZeppelinComm
from .comm_manager import ZeppelinCommManager


INTERACTIVE = False

class JupyterShim:
    
    class _JupyterShim:
    
        def __init__(self, wsServer):
            self._loadJsLibs()
            self.comm = ZeppelinNotebookComm(wsServer, self)
            self.comm_manager = ZeppelinCommManager()

            from IPython.core.interactiveshell import InteractiveShell
            InteractiveShell.instance().display_pub = ZeppelinDisplayPublisher(self)
            
            import ipykernel.comm
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager
            
            print("JupyterShim initialized")

        def _loadJsLibs(self):
            scripts = "<script>"
            if INTERACTIVE:
                scripts += WSJS
            else:
                for script in ["comm.js", "comm_manager.js", "notebook_comm.js", "kernel.js", "notebook.js"]:
                    scripts += open("%s/js/%s" % (dirname(__file__), script), "r").read()
                    scripts += "\n"

            scripts += "</script>"
            self._print(scripts, True)
            
        def _print(self, html, header=False):
            if header: print("%html")
            print(html)
        
        def _printJs(self, script, header=False):
            wrapper = "<script>" + script + "</script>"
            self._print(wrapper, header)
            
        def publish(self, html, header=True, default=""):
            div_id = str(uuid4())
            wrapper = '<div id="%s">%s</div>' % (div_id, default)
            self._print(wrapper, header)
            self.comm.send("publish", {"div_id":div_id, "html":html})


    instance = None

    def __init__(self, wsServer="ws://localhost:9001"):
        if not JupyterShim.instance:
            JupyterShim.instance = JupyterShim._JupyterShim(wsServer)

    def __getattr__(self, name):
        return getattr(self.instance, name)

