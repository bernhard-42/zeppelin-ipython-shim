from .comm import ZeppelinComm

class ZeppelinCommManager:

    def __init__(self):
        self.targets = {}
        self.comms = {}

    def register_target(self, target_name, f):
        self.targets[target_name] = f

    def unregister_target(self, target_name, f):
        return self.targets.pop(target_name)

    def register_comm(self, comm):
        comm_id = comm.comm_id
        self.comms[comm_id] = comm
        return comm_id

    def unregister_comm(self, comm):
        comm = self.comms.pop(comm.comm_id)

    def get_comm(self, comm_id):
        return self.comms[comm_id]

    def comm_open(self, stream, ident, msg):
        content = msg['content']
        comm_id = content['comm_id']
        target_name = content['target_name']

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
        try:
            comm.handle_msg(msg)
        except Exception:
            print('Exception in comm_msg for %s', comm_id)

    def comm_close(self, stream, ident, msg):
        """Handler for comm_close messages"""
        content = msg['content']
        comm_id = content['comm_id']
        comm = self.get_comm(comm_id)

        del self.comms[comm_id]

        try:
            comm.handle_close(msg)
        except Exception:
            print('Exception in comm_close for %s', comm_id)
