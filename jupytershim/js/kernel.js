/**
  *  class Kernel
  */

var Kernel = function (notebook, wsServer) {
  console.info("Kernel: init, wsServer: " + wsServer);
  this.notebook = notebook;
  this.notebookComm = new ZeppelinNotebookComm(this, notebook.notebook_id, wsServer);
  this.comm_manager = new CommManager(this);
}

Kernel.prototype.send_shell_msg = function(msg_type, content, callbacks, metadata, buffers) {
  this.notebookComm.send(msg_type, content);
}
