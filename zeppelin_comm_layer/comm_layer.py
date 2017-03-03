import logging

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
        
        self.logger.debug("Patching ipykernel Comm and CommManager")
        ipykernel.comm.Comm = ZeppelinComm
        ipykernel.comm.CommManager = ZeppelinCommManager
        
        self.ip = InteractiveShell.instance()
        session = ZeppelinSession(self, self.zeppelinContext)
        commManager = ZeppelinCommManager()
        self.logger.debug("Patching InteractiveShell.kernel")
        self.ip.kernel = Kernel(commManager, session)

        self.logger.debug("Setting IPython Display Manager")
        self.ip.display_pub = ZeppelinDisplayPublisher(session)
        
        self.ip.kernel.session.init()

    def start(self):
        self.logger.info("Starting Comm Layer Watcher")
        self.ip.kernel.session.start()
               
    def enableBokeh(self):
        BokehStates(self.zeppelinContext).initState()


def resetZeppelinCommLayer(zeppelinContext):
    noteId = zeppelinContext.getInterpreterContext().getNoteId()
    sessionCommVar = "____zeppelin_comm_%s_msg__" % noteId
    zeppelinContext.angularBind(sessionCommVar, {"task":"reset", "msg":{}})
    zeppelinContext.angularUnbind(sessionCommVar)
