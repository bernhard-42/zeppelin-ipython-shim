/**
  *  class Notebook
  */

var Notebook = function (jupyter) {
  console.info("Notebook: init");
  this.jupyter = jupyter;
  this.kernel = new Kernel(this);
}