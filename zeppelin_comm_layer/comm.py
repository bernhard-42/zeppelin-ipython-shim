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
import sys
if sys.version_info.major == 2:
    import zeppelin_comm_layer
else:
    from . import zeppelin_comm_layer


class ZeppelinComm:
    
    def __init__(self, target_name, data=None, metadata=None):
        self.target_name = target_name
        self.data = data
        self.metadata = metadata
        self.comm_id = str(uuid4())
        self._closed = False
        self._close_callback = None
        self._msg_callback = None
        self.kernel = zeppelin_comm_layer.ZeppelinCommLayer().ip.kernel
        self.open(data, metadata)

    def _send(self, task, data, metadata):
        msg = {"comm_id":self.comm_id, "target_name":self.target_name, "data":data, "metadata":metadata}
        self.kernel.session.send(task, msg)

    def open(self, data=None, metadata=None):
        comm_manager = self.kernel.comm_manager
        comm_manager.register_comm(self)
        self._send("comm_open", data, metadata)

    def close(self, data=None, metadata=None):
        if not self._closed:
            self._closed = True
            self._send("comm_close", data, metadata)

    def send(self, data=None, metadata=None, buffers=None):
        self._send("comm_msg", data, metadata)

    def on_close(self, callback):
        self._close_callback = callback

    def on_msg(self, callback):
        self._msg_callback = callback

    def handle_close(self, msg):
        if self._close_callback:
            self._close_callback(msg)

    def handle_msg(self, msg):
        if self._msg_callback:
            self._msg_callback(msg)