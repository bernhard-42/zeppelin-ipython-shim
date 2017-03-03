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

from .comm import ZeppelinComm
from .logger import Logger
from .utils import Singleton
from six import with_metaclass


class ZeppelinCommManager(with_metaclass(Singleton)):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.info("New ZeppelinCommManager")

        self.targets = {}
        self.comms = {}
        
    def register_target(self, target_name, f):
        self.logger.debug("Registering target %s" % target_name)
        self.targets[target_name] = f

    def unregister_target(self, target_name, f):
        self.logger.debug("Unregistering target %s" % target_name)
        return self.targets.pop(target_name)

    def register_comm(self, comm):
        self.logger.debug("Registering comm %s" % comm.comm_id)
        comm_id = comm.comm_id
        self.comms[comm_id] = comm
        return comm_id

    def unregister_comm(self, comm):
        self.logger.debug("Unregistering comm %s" % comm.comm_id)
        comm = self.comms.pop(comm.comm_id)

    def get_comm(self, comm_id):
        self.logger.debug("Get comm %s" % comm.comm_id)
        return self.comms[comm_id]

    def comm_open(self, stream, ident, msg):
        content = msg['content']
        comm_id = content['comm_id']
        target_name = content['target_name']
        self.logger.debug("Opening a Comm for target_name %s and com_id %s" % (target_name, comm_id))

        comm = ZeppelinComm(comm_id=comm_id, target_name=target_name)
        self.register_comm(comm)

        f = self.targets.get(target_name, None)
        try:
            f(comm, msg)
            return
        except Exception:
            print("Exception opening comm with target: %s", target_name)

        # Failure.
        try:
            comm.close()
        except:
            pass

    def comm_msg(self, stream, ident, msg):
        """Handler for comm_msg messages"""
        content = msg['content']
        comm_id = content['comm_id']
        comm = self.get_comm(comm_id)
        self.logger.debug("Handle msg for com_id %s: %s" % (comm_id, msg))
        try:
            comm.handle_msg(msg)
        except Exception:
            print('Exception in comm_msg for %s', comm_id)

    def comm_close(self, stream, ident, msg):
        """Handler for comm_close messages"""
        content = msg['content']
        comm_id = content['comm_id']
        comm = self.get_comm(comm_id)
        self.logger.debug("Closing comm %s" % comm_id)

        del self.comms[comm_id]

        try:
            comm.handle_close(msg)
        except Exception:
            print('Exception in comm_close for %s', comm_id)