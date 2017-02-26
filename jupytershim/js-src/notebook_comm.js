/**
  *  class ZeppelinNotebookComm
  */

var ZeppelinNotebookComm = function(kernel) {
    console.info("ZeppelinNotebookComm: init");
    this.kernel = kernel;
}   

ZeppelinNotebookComm.prototype.handleMsg = function(data) {
    if(data.task == "publish") {
        this.publish(data.msg.div_id, data.msg.html);
    } else if(data.task == "comm_open") {
        var msg = data.msg;
        this.kernel.comm_manager.new_comm(msg.target_name, msg.data, {}, msg.metadata, msg.comm_id)
    } else if(data.task == "comm_close") {
        console.log("comm_close:");
        console.log(data);
    } else if(data.task == "comm_msg") {
        var msg = data.msg;
        this.kernel.comm_manager.comms[msg.comm_id].then(function(comm) {
            comm.handle_msg({"content": msg}); 
        });
    } else {
        console.error("UNHANDLED:" + JSON.stringify(data));
    }
}

ZeppelinNotebookComm.prototype.send = function(task, msg) {
    console.info("ZeppelinNotebookComm: send " + task);
    this.zeppelinWS.send(JSON.stringify({"notebook_id":this.notebookId, "task": task, "node":"notebook", "msg":msg}));
}

ZeppelinNotebookComm.prototype.publish = function(div_id, html) {
    console.info("ZeppelinNotebookComm: publish " + div_id);

    var counter = 0;

    // Sometimes the communication call is faster than printing the DIV, so retry ...
    var retryId = setInterval(function() {
        div = document.getElementById(div_id);
        if (div !== null) {
            clearInterval(retryId);

            // add html, script or html+script
            div.innerHTML = html;

            // Force execution of all scripts
            scripts = div.getElementsByTagName("script");
            for(i in scripts) {
                eval(scripts[i].innerHTML);
            }
        }

        // maximum 2 seconds
        if (counter == 10) {
            clearInterval(retryId);
        }
    }, 200);
}
