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
from .enable_bokeh import BokehStates
from .enable_vegalite import VegaLite


class ZeppelinCommLayer:
    __version__ = "0.9.1"

    def __init__(self, zeppelinContext, logLevel):

        LogLevel().setLogLevel(logLevel)
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.propagate = False        
        self.logger.info("Initializing ZeppelinCommLayer")

        self.zeppelinContext = zeppelinContext
        
        self.logger.debug("Patching ipykernel Comm and CommManager")
        ipykernel.comm.Comm = ZeppelinComm
        ipykernel.comm.CommManager = ZeppelinCommManager
        
        self.logger.info("Loading Comm Layer Javascript libs")
        jsScript = open("%s/js/zeppelin_comm_layer-min.js" % dirname(__file__), "r").read() + "\nconsole.log('Comm Layer Javascript libs loaded')"

        self.ip = InteractiveShell.instance()
        self.session = ZeppelinSession(self.zeppelinContext, jsScript)
        commManager = ZeppelinCommManager()
        self.logger.debug("Patching InteractiveShell.kernel")
        self.ip.kernel = Kernel(commManager, self.session)

        self.logger.debug("Setting IPython Display Manager")
        self.ip.display_pub = ZeppelinDisplayPublisher(self.session)
        
        self.ip.kernel.session.init()

    def start(self):
        self.logger.info("Starting Comm Layer Watcher")
        self.ip.kernel.session.start()
               
    def enableBokeh(self):
        BokehStates(self.zeppelinContext).initState()

    def enableVegaLite(self):
        vg = VegaLite(self.session)
        return vg

    def reset(self):
        self.session.reset()

