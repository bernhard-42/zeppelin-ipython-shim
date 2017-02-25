/**
  *  class Kernel
  */

var Kernel = function (notebook) {
  console.info("Kernel: init");
  this.notebook = notebook;
  this.notebookComm = new ZeppelinNotebookComm(this);
  this.comm_manager = new CommManager(this);
}

Kernel.prototype.send_shell_msg = function(msg_type, content, callbacks, metadata, buffers) {
  this.notebookComm.send(msg_type, content);
}