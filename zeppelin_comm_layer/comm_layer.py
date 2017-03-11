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


import logging
import time
from uuid import uuid4
from os.path import dirname 

from IPython.core.interactiveshell import InteractiveShell
import ipykernel.comm

from .display_pub import ZeppelinDisplayPublisher
from .comm_manager import ZeppelinCommManager
from .comm import ZeppelinComm
from .kernel import Kernel
from .utils import Singleton
from .logger import Logger


__ZEPPELIN_COMM_LAYER = {}


_JUPYTER_HANDLER = """
__jupyterHandler = function(session, object) {
    Jupyter.notebook.kernel.session.handleMsg(object);
}
"""


def ZeppelinCommLayer(zeppelinContext, _tag="%angular", _logLen=400):

    class ZeppelinCommLayer:
        __version__ = "0.9.3"

        def __init__(self, zeppelinContext, _tag="%angular", _logLen=400):

            self.logger = Logger(self.__class__.__name__, size=_logLen).get()
            self.logger.propagate = False        
            self.logger.info("Initializing ZeppelinCommLayer")

            self._tag = _tag
            self.zeppelinContext = zeppelinContext
            self.commLayerId = str(uuid4())
            
            #
            # Load javascript classes Notbook, Kernel, Session, comm and CommManager simulating
            # IPython Javascript communication part
            #
            self.logger.info("Loading Comm Layer Javascript libs")
            jsScript = open("%s/js/zeppelin_comm_layer-min.js" % dirname(__file__), "r").read()
            self.logger.debug(jsScript)
            print(_tag)
            print("""<script>{{%s}}</script>\n""" % jsScript)

            #
            # Add the new Kernel object to IPythons InteractiveShell so that CommManager is 
            # accessible by libraries that use IPython's communication system
            #
            self.kernel = Kernel(self.zeppelinContext, _logLen)
            self.logger.info("Patching InteractiveShell.kernel")
            self.ip = InteractiveShell.instance()
            self.ip.kernel = self.kernel

            #
            # Set global entry points for libraries commiunicating via IPython
            #
            self.logger.info("Patching ipykernel Comm and CommManager")
            ipykernel.comm.Comm = ZeppelinComm
            ipykernel.comm.CommManager = ZeppelinCommManager

            #
            # Add the new displqyPublisher instance to IPythons display_pub so that libraries 
            # that use IPython's display system can write to Zeppelin
            #
            self.logger.debug("Setting IPython Display Manager")
            self.ip.display_pub = ZeppelinDisplayPublisher(self.kernel)
        
        #
        # needs to be called every time ZeppelinCommLayer() gets called to initialize the 
        # ZeppelinSession, see wrapping factory function
        #
        def init(self):
            self.kernel.initSession(self._tag)


        def start(self, _tag="%angular"):
            self.logger.info("Starting Comm Layer Watcher")
            self.kernel.startSession(_tag)
            time.sleep(0.5)
            self.kernel.registerFunction("__jupyterHandler", _JUPYTER_HANDLER)  

                   
        def _reset(self):
            # self.zeppelinContext.angularBind(sessionCommVar, {"task":"comm_reset", "msg":{}})
            self.kernel.send("comm_reset", {})
            time.sleep(0.5)
            self.kernel.resetSession()


    #
    # Factory, only return one ZeppelinCommLayer for each Zeppelin notebook
    #

    global __ZEPPELIN_COMM_LAYER

    logger = Logger("ZeppelinCommLayerFactory").get()

    noteId = zeppelinContext.getInterpreterContext().getNoteId()
    logger.debug("Requesting Comm Layer for Notebook %s (%s)" % 
                    (noteId, "None" if not __ZEPPELIN_COMM_LAYER.get(noteId)
                                    else __ZEPPELIN_COMM_LAYER.get(noteId).commLayerId))

    if __ZEPPELIN_COMM_LAYER.get(noteId) is None:
        __ZEPPELIN_COMM_LAYER[noteId] = ZeppelinCommLayer(zeppelinContext, _tag, _logLen)
    
    logger.debug("Notebook: %s ZeppelinCommLayer: %s (Session ID: %s)" %
                    (noteId, 
                     __ZEPPELIN_COMM_LAYER.get(noteId).commLayerId,
                     __ZEPPELIN_COMM_LAYER.get(noteId).kernel.getSessionId()))
    
    # Force ZeppelinSession.init()
    __ZEPPELIN_COMM_LAYER[noteId].init()

    return __ZEPPELIN_COMM_LAYER[noteId]


def resetZeppelinCommLayer(zeppelinContext):
    noteId = zeppelinContext.getInterpreterContext().getNoteId()
    if __ZEPPELIN_COMM_LAYER.get(noteId) is not None:
        __ZEPPELIN_COMM_LAYER.get(noteId)._reset()
        __ZEPPELIN_COMM_LAYER[noteId] = None 
