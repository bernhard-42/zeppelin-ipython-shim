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
  *  class Comm
  */

var Comm = function (target_name, comm_id) {
    console.info("Comm: Init");
    this.target_name = target_name;
    this.comm_id = comm_id || utils.uuid();
    this._msg_callback = this._close_callback = null;
};

// methods for sending messages
Comm.prototype.open = function (data, callbacks, metadata) {
  console.error("Comm.open is not implemented yet")
  return None;
};

Comm.prototype.send = function (data, callbacks, metadata, buffers) {
  console.error("Comm.send is not implemented yet")
  return None;
};

Comm.prototype.close = function (data, callbacks, metadata) {
  console.error("Comm.close is not implemented yet")
  return None;
};

Comm.prototype._register_callback = function (key, callback) {
    console.info("Comm: register_callback for " + key);
    this['_' + key + '_callback'] = callback;
};

Comm.prototype.on_msg = function (callback) {
    console.info("Comm: on_msg");
    this._register_callback('msg', callback);
};

Comm.prototype.on_close = function (callback) {
    console.info("Comm: on_close");
    this._register_callback('close', callback);
};

Comm.prototype._callback = function (key, msg) {
    console.info("Comm: _callback for " + key);
    var callback = this['_' + key + '_callback'];
    if (callback) {
        try {
            callback(msg);
        } catch (e) {
            console.log("Exception in Comm callback", e, e.stack, msg);
        }
    }
};

Comm.prototype.handle_msg = function (msg) {
    console.info("Comm: handle_msg");
    this._callback('msg', msg);
};

Comm.prototype.handle_close = function (msg) {
    console.info("Comm: handle_close");
    this._callback('close', msg);
};

