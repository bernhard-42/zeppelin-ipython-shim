from uuid import uuid4
from os.path import dirname 
from .notebook_comm import ZeppelinNotebookComm
from .display_pub import ZeppelinDisplayPublisher
from .comm import ZeppelinComm
from .comm_manager import ZeppelinCommManager
from .kernel import Kernel


INTERACTIVE = False

class JupyterShim:

    class _JupyterShim:
    
        def __init__(self, wsServer):
            self._loadJsLibs()

            from IPython.core.interactiveshell import InteractiveShell
            ip = InteractiveShell.instance()
            ip.display_pub = ZeppelinDisplayPublisher(self)
            
            session = ZeppelinNotebookComm(wsServer, self)
            commManager = ZeppelinCommManager()
            kernel = Kernel(commManager, session)
            ip.kernel = kernel

            import ipykernel.comm
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager
            
            self.ip = ip

            print("JupyterShim initialized")

        def _loadJsLibs(self):
            scripts = "<script>"
            for script in ["comm.js", "comm_manager.js", "notebook_comm.js", "notebook.js", "kernel.js"]:
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
            
        def publish(self, html, header=True, default="", div_id=None):
            if not div_id:
                div_id = self.placeholder(header, default)
            self.ip.kernel.session.send("publish", {"div_id":div_id, "html":html})
            
        def placeholder(self, header=True, default=""):
            div_id = str(uuid4())
            wrapper = '<div id="%s">%s</div>' % (div_id, default)
            self._print(wrapper, header)
            return div_id
            
    instance = None

    def __init__(self, wsServer="ws://localhost:9001"):
        if not JupyterShim.instance:
            JupyterShim.instance = JupyterShim._JupyterShim(wsServer)

    def __getattr__(self, name):
        return getattr(self.instance, name)