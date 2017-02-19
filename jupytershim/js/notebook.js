/**
  *  class Notebook
  */

var Notebook = function (jupyter, notebook_id, wsServer) {
  console.info("Notebook: init, notebookId: " + notebook_id + " wsServer: " + wsServer);
  this.jupyter = jupyter;
  this.notebook_id = notebook_id;
  this.kernel = new Kernel(this, wsServer);
}
