from uuid import uuid4

class ZeppelinComm:
    
    def __init__(self, target_name, data=None, metadata=None):
        self.target_name = target_name
        self.data = data
        self.metadata = metadata
        self.comm_id = str(uuid4())
        self._closed = False
        self._close_callback = None
        self._msg_callback = None
        self.jupyterShim = JupyterShim()
        self.open(data, metadata)

    def _send(self, task, data, metadata):
        msg = {"comm_id":self.comm_id, "target_name":self.target_name, "data":data, "metadata":metadata}
        self.jupyterShim.comm.send(task, msg)

    def open(self, data=None, metadata=None):
        comm_manager = self.jupyterShim.comm_manager
        comm_manager.register_comm(self)
        self._send("comm_open", data, metadata)

    def close(self, data=None, metadata=None):
        if not self._closed:
            self._closed = True
            self._send("comm_close", data, metadata)

    def send(self, data=None, metadata=None):
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

