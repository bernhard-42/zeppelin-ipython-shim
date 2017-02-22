/**
  *  class ZeppelinNotebookComm
  */

var ZeppelinNotebookComm = function(kernel, notebookId, wsServer) {
    console.info("ZeppelinNotebookComm: init, notebookId: " + notebookId + " wsServer: " + wsServer);
    this.kernel = kernel;
    this.notebookId = notebookId;
    console.info("Init ZeppelinNotebookComm " + notebookId);
   
    that = this;

    this.zeppelinWS = new WebSocket(wsServer);
        
    this.zeppelinWS.onmessage = function(event) {
        var data = JSON.parse(event.data);
        if(data.task == "publish") {
            that.publish(data.msg.div_id, data.msg.html);
        } else if(data.task == "comm_open") {
            var msg = data.msg;
            that.kernel.comm_manager.new_comm(msg.target_name, msg.data, {}, msg.metadata, msg.comm_id)
        } else if(data.task == "comm_close") {
            console.log("comm_close:");
            console.log(data);
        } else if(data.task == "comm_msg") {
            var msg = data.msg;
            that.kernel.comm_manager.comms[msg.comm_id].then(function(comm) {
                comm.handle_msg({"content": msg}); 
            });
        } else {
            console.log("UNHANDLED:");
            console.log(data);
        }
    };

    this.zeppelinWS.onopen = function (event) {
        that.send("init", "initialize");
    };

    window._jupyter_comms.comm = this;
}

ZeppelinNotebookComm.prototype.send = function(task, msg) {
    console.info("ZeppelinNotebookComm: send " + task);
    this.zeppelinWS.send(JSON.stringify({"notebook_id":this.notebookId, "task": task, "node":"notebook", "msg":msg}));
}

ZeppelinNotebookComm.prototype.publish = function(div_id, html) {
    console.info("ZeppelinNotebookComm: publish " + div_id);
    setTimeout(function(){
        div = document.getElementById(div_id);
        div.innerHTML = html;
    }, 100);
}
