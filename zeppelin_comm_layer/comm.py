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
from .logger import Logger, LogLevel
import sys
from IPython.core.interactiveshell import InteractiveShell


class ZeppelinComm:
    
    def __init__(self, target_name, data=None, metadata=None):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.info("New ZeppelinComm for target %s" % target_name)

        self.target_name = target_name
        self.data = data
        self.metadata = metadata
        self.comm_id = str(uuid4())
        self._closed = False
        self._close_callback = None
        self._msg_callback = None
        self.kernel = InteractiveShell.instance().kernel

        self.open(data, metadata)

    def _send(self, task, data, metadata):
        self.logger.debug("Send for target %s" % self.target_name)
        msg = {"comm_id":self.comm_id, "target_name":self.target_name, "data":data, "metadata":metadata}
        self.kernel.session.send(task, msg)

    def open(self, data=None, metadata=None):
        self.logger.debug("Register Comm %s with CommManager ..." % self.comm_id)
        comm_manager = self.kernel.comm_manager
        comm_manager.register_comm(self)
        self.logger.debug("... and send comm_open for %s to notebook" % self.comm_id)
        self._send("comm_open", data, metadata)

    def close(self, data=None, metadata=None):
        self.logger.debug("Close Comm %s ..." % self.comm_id)
        if not self._closed:
            self._closed = True
            self.logger.debug("... and send comm_close for %s to notebook" % self.comm_id)
            self._send("comm_close", data, metadata)

    def send(self, data=None, metadata=None, buffers=None):
        self.logger.debug("Send comm_msg for %s with data=%s and metadata=%s" % (self.comm_id, data, metadata))
        self._send("comm_msg", data, metadata)

    def on_close(self, callback):
        self.logger.debug("Set on_close for %s" % self.comm_id)
        self._close_callback = callback

    def on_msg(self, callback):
        self.logger.debug("Set on_msg for %s" % self.comm_id)
        self._msg_callback = callback

    def handle_close(self, msg):
        self.logger.debug("Handle_close for %s" % self.comm_id)
        if self._close_callback:
            self._close_callback(msg)

    def handle_msg(self, msg):
        self.logger.debug("Handle_msg for %s" % self.comm_id)
        if self._msg_callback:
            self._msg_callback(msg)
