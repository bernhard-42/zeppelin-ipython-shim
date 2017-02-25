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
            self._loadJsLibs()
            self.zeppelinContext = zeppelinContext
            
            from IPython.core.interactiveshell import InteractiveShell
            ip = InteractiveShell.instance()
            ip.display_pub = ZeppelinDisplayPublisher(self)
            
            session = ZeppelinNotebookComm(self, zeppelinContext, debug)
            commManager = ZeppelinCommManager()
            kernel = Kernel(commManager, session)
            ip.kernel = kernel

            import ipykernel.comm
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager
            
            self.ip = ip

        def _loadJsLibs(self):
            scripts = "<script>"
            for script in ["comm.js", "comm_manager.js", "notebook_comm.js", "notebook.js", "kernel.js"]:
                scripts += open("%s/js/%s" % (dirname(__file__), script), "r").read()
                scripts += "\n"
            scripts += "</script>"
            self._print(scripts, True)

            
        def _print(self, html, header=False):
            if header: print("%angular")
            print(html)
        
        def _printJs(self, script, header=False):
            wrapper = "<script>" + script + "</script>"
            self._print(wrapper, header)

    instance = None

    def __init__(self, zeppelinContext=None, debug=False):
        if not JupyterShim.instance:
            JupyterShim.instance = JupyterShim._JupyterShim(zeppelinContext, debug)
            
    def __getattr__(self, name):
        return getattr(self.instance, name)


def jupyterReset():
    print("%angular <script>Jupyter=null;</script>")
    JupyterShim.instance = None