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
  *  class CommManager
  */

var CommManager = function (kernel) {
  console.info("CommManager: Init");
  this.kernel = kernel;
  this.comms = {};
  this.targets = {};
};

CommManager.prototype.new_comm = function (target_name, data, callbacks, metadata, comm_id) {
    if(typeof comm_id === "undefined") {
        console.error("CommManager: new_comm with new comm_id not implemented yet");
        return
    }
    
    console.info("CommManager: new_comm target: " + target_name + " comm_id: " + comm_id);
    var comm = new Comm(target_name, comm_id);
    this.register_comm(comm);
    
    if(typeof comm_id === "undefined") {
        comm.open(data, callbacks, metadata);
    }
    return comm;
};

CommManager.prototype.register_target = function (target_name, f) {
    console.info("CommManager: register_target: " + target_name);
    this.targets[target_name] = f;
};

CommManager.prototype.unregister_target = function (target_name, f) {
    console.info("CommManager: unregister_target: " + target_name);
    delete this.targets[target_name];
};

CommManager.prototype.register_comm = function (comm) {
    console.info("CommManager: register_comm comm_id: " + comm.comm_id);
    this.comms[comm.comm_id] = Promise.resolve(comm);
    comm.kernel = this.kernel;
    return comm.comm_id;
};

CommManager.prototype.unregister_comm = function (comm) {
    console.info("CommManager: unregister_comm comm_id: " + comm.comm_id);
    delete this.comms[comm.comm_id];
};

CommManager.prototype.comm_open = function (msg) {
  console.error("CommManager.comm_open is not implemented yet")
  return None;
};

CommManager.prototype.comm_close = function(msg) {
  console.error("CommManager.comm_close is not implemented yet")
  return None;
};

CommManager.prototype.comm_msg = function(msg) {
  console.error("CommManager.comm_msg is not implemented yet")
  return None;
};
