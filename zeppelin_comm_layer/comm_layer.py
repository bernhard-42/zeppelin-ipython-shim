from uuid import uuid4
import logging
from os.path import dirname 

from IPython.core.interactiveshell import InteractiveShell
import ipykernel.comm

from .session import ZeppelinSession
from .display_pub import ZeppelinDisplayPublisher
from .comm import ZeppelinComm
from .comm_manager import ZeppelinCommManager
from .kernel import Kernel
from .utils import Singleton
from .logger import Logger, LogLevel
from .bokeh_state import BokehStates


class ZeppelinCommLayer:

    def __init__(self, zeppelinContext, logLevel):

        LogLevel().setLogLevel(logLevel)
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.info("Initializing ZeppelinCommLayer singleton")

        self.zeppelinContext = zeppelinContext
        self._loadJsLibs()
        
        self.ip = InteractiveShell.instance()
        
        self.logger.debug("Patching InteractiveShell.kernel")
        session = ZeppelinSession(self, self.zeppelinContext)
        commManager = ZeppelinCommManager()
        kernel = Kernel(commManager, session)
        self.ip.kernel = kernel

        self.logger.debug("Patching ipykernel Comm and CommManager")
        ipykernel.comm.Comm = ZeppelinComm
        ipykernel.comm.CommManager = ZeppelinCommManager

        self.logger.debug("Setting IPython Display Manager")
        self.ip.display_pub = ZeppelinDisplayPublisher(self)
        
    def start(self):
        self.logger.info("Starting Comm Layer Watcher")
        self.ip.kernel.session.start()
        
    def _loadJsLibs(self):
        self.logger.info("Loading Comm Layer Javascript libs")
        jsScript = open("%s/js/zeppelin_comm_layer-min.js" % dirname(__file__), "r").read() + "\n"
        self._printJs(jsScript, header=True, delayed=False)
        
    def _print(self, html, header=False, delayed=True):
        if delayed:
            if header:
                print("%angular")
            div_id = str(uuid4())
            wrapper = '<div id="%s"></div>' % div_id
            print(wrapper)
            self.logger.debug("Delayed printing of " + wrapper)
            self.ip.kernel.session.send("publish", {"div_id":div_id, "html":html})
        else:
            self.logger.debug("Immediate printing of " + html)
            if header:
                print("%html")
            print(html)
    
    def _printJs(self, script, header=False, delayed=True):
        wrapper = '<script type="text/javascript">' + script + '</script>'
        self._print(wrapper, header, delayed)

    def enableBokeh(self):
        BokehStates(self.zeppelinContext).initState()


def resetZeppelinCommLayer(zeppelinContext):
    noteId = zeppelinContext.getInterpreterContext().getNoteId()
    sessionCommVar = "____zeppelin_comm_%s_msg__" % noteId
    zeppelinContext.angularBind(sessionCommVar, {"task":"reset", "msg":{}})
    zeppelinContext.angularUnbind(sessionCommVar)
