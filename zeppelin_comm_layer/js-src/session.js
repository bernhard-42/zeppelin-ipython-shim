/**
  * Copyright 2017 Bernhard Walter
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *    http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  */

/**
  *  class ZeppelinSession
  */

var ZeppelinSession = function(kernel) {
    console.info("ZeppelinSession: init");
    this.kernel = kernel;
}   

ZeppelinSession.prototype.handleMsg = function(object) {
    if(object.task == "publish") {
        this.publish(object.msg.div_id, object.msg.html); 
    } else if(object.task == "comm_reset") {
        console.log("cleaning watchers")
        var unwatchers = window.__zeppelin_notebook_unwatchers__;
        for(i in unwatchers) {
            unwatchers[i]();
        }
        window.__zeppelin_notebook_unwatchers__ = [];
        window.__zeppelin_already_executed__ = [];
        console.log("Deleting Jupyter")
        Jupyter = null;
    } else if(object.task == "comm_open") {
        var msg = object.msg;
        console.info("Open comm for target_name" + msg.target_name + "and comm id " + msg.comm_id);
        this.kernel.comm_manager.new_comm(msg.target_name, msg.object, {}, msg.metadata, msg.comm_id)
    } else if(object.task == "comm_close") {
        console.log("comm_close:");
        console.log(object);
    } else if(object.task == "comm_msg") {
        var msg = object.msg;
        console.info("Message for comm id " + msg.comm_id);
        this.kernel.comm_manager.comms[msg.comm_id].then(function(comm) {
            comm.handle_msg({"content": msg}); 
        });
    } else {
        console.error("UNHANDLED:" + JSON.stringify(object));
    }
}

ZeppelinSession.prototype.send = function(task, msg) {
    console.info("ZeppelinSession: send " + task);
    console.error("Not implemented yet");
}

ZeppelinSession.prototype.publish = function(div_id, html) {
    console.info("ZeppelinSession: publish " + div_id);

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
