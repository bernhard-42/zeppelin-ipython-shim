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


