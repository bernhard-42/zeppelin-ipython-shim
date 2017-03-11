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

from zeppelin_session import ZeppelinSession
from .comm_manager import ZeppelinCommManager
from .logger import Logger

class Kernel:

    #
    # The session will be created or retreived (zeppelin_session module) and a new 
    # CommManger gets created.
    #

    def __init__(self, zeppelinContext, _logLen):
        self.logger = Logger(self.__class__.__name__, size=_logLen).get()
        
        self.logger.info("Create ZeppelinSession")
        self.session = ZeppelinSession(zeppelinContext)
        
        self.logger.info("Create CommManager")
        self.comm_manager = ZeppelinCommManager()

    def initSession(self, _tag):
        self.session.init(_tag)

    def startSession(self, _tag):
        self.session.start(_tag)

    def resetSession(self):
        self.session._reset()

    def getSessionId(self):
        return self.session.sessionId
        
    def registerFunction(self, name, jsFunc):
        self.session.registerFunction(name, jsFunc)

    def unregisterFunction(self, name):
        self.session.unregisterFunction(name)

    def send(self, task, msg):
        self.session.call("__jupyterHandler", {"task":task, "msg":msg})

            