## 1 Import the Zeppelin Comm Layer, intialize it ...

### 1.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark

from zeppelin_session import ZeppelinSession, resetZeppelinSession, LogLevel

# resetZeppelinSession(z.z)
LogLevel().setLogLevel("DEBUG")

session = ZeppelinSession(z.z)
session.init()
```

### 1.2 Zeppelin Comm Layer Log File

```
2017-03-11 19:18:14,512 DEBUG:ZeppelinCommLayerFactory Requesting Comm Layer for Notebook 2C9HR8ADP (None)
2017-03-11 19:18:14,512 INFO:ZeppelinCommLayer Initializing ZeppelinCommLayer
2017-03-11 19:18:14,513 INFO:ZeppelinCommLayer Loading Comm Layer Javascript libs
2017-03-11 19:18:14,513 DEBUG:ZeppelinCommLayer var Comm=function(target_name,comm_id){console.info("Comm: Init");this.target_name=target_name;this.comm_id=comm_id||utils.uuid();this._msg_callback=this._close_callback=null};Comm.prototype.open=function(data,callbacks,metadata){console.error("Comm.open is not implemented yet");return None};Comm.prototype.send=function(data,callbacks,metadata,buffers){console.error("Comm.send is not impleme [...(4667)]
2017-03-11 19:18:14,518 INFO:Kernel Create ZeppelinSession
2017-03-11 19:18:14,520 INFO:ZeppelinSession New ZeppelinSession 072f8c9f-4b12-4a1d-a9f6-b8a5a9eb3dd5
2017-03-11 19:18:14,520 INFO:Kernel Create CommManager
2017-03-11 19:18:14,520 INFO:ZeppelinCommManager New ZeppelinCommManager
2017-03-11 19:18:14,520 INFO:ZeppelinCommLayer Patching InteractiveShell.kernel
2017-03-11 19:18:14,596 INFO:ZeppelinCommLayer Patching ipykernel Comm and CommManager
2017-03-11 19:18:14,597 DEBUG:ZeppelinCommLayer Setting IPython Display Manager
2017-03-11 19:18:14,597 INFO:ZeppelinDisplayPublisher New ZeppelinDisplayManager
2017-03-11 19:18:14,597 DEBUG:ZeppelinCommLayerFactory Notebook: 2C9HR8ADP ZeppelinCommLayer: 4431b561-e8b6-43cc-bbad-fbcd00627715 (Session ID: 072f8c9f-4b12-4a1d-a9f6-b8a5a9eb3dd5)
2017-03-11 19:18:14,597 INFO:ZeppelinSession Initializing ZeppelinSession 072f8c9f-4b12-4a1d-a9f6-b8a5a9eb3dd5
```

### 1.3 Browser Web Console

```
Comm Layer Javascript libs loaded
Initiate Javascript part of Zeppelin Comm Layer
Notebook: init
Kernel: init
ZeppelinSession: init
CommManager: Init
```


## 2 ... and start it in the next (!) Zeppelin paragraph

### 2.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark

zcl.start()
```

### 2.2 Zeppelin Comm Layer Log File

```
2017-03-11 19:19:25,797 INFO:ZeppelinCommLayer Starting Comm Layer Watcher
2017-03-11 19:19:26,317 INFO:ZeppelinSession Register function __jupyterHandler with: \n__jupyterHandler = function(session, object) {\n    Jupyter.notebook.kernel.session.handleMsg(object);\n}\n
```

### 2.3 Browser Web Console

```
Get scope for div id__Zeppelin_Session_2C9HR8ADP_Comm__
Install Angular watcher for session comm var __zeppelin_comm_2C9HR8ADP_msg__
Registering function __jupyterHandler
```


## 3 Load Bokeh libraries and redirect output to Zeppelin Notebook

### 3.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.resources import Resources
from bokeh.plotting import figure

output_notebook()
```

### 3.2 Zeppelin Comm Layer Log File

```
2017-03-11 19:21:24,563 DEBUG:ZeppelinDisplayPublisher Publish html \n    <div class="bk-root">\n        <a href="http://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>\n        <span id="c88ad21b-75c3-4b88-9fad-6332ceb1e126">Loading BokehJS ...</span>\n    </div>
2017-03-11 19:21:24,564 DEBUG:ZeppelinDisplayPublisher Delayed printing of <div id="b7dcfee9-94e8-455b-baaf-d68f467315e4"></div>
2017-03-11 19:21:24,574 DEBUG:ZeppelinDisplayPublisher Publish javascript \n(function(global) {\n  function now() {\n    return new Date();\n  }\n\n  var force = true;\n\n  if (typeof (window._bokeh_onload_callbacks) === "undefined" || force === true) {\n    window._bokeh_onload_callbacks = [];\n    window._bokeh_is_loading = undefined;\n  }\n\n\n  \n  if (typeof (window._bokeh_timeout) === "undefined" || force === true) {\n    window._bokeh_timeout = Date.now( [...(4379)]
2017-03-11 19:21:24,574 DEBUG:ZeppelinDisplayPublisher Delayed printing of <div id="513e39b4-5d7b-49c3-9131-9722abfa426a"></div>
```


### 3.3 Browser Web Console

```
Calling function __jupyterHandler with delay: 200
ZeppelinSession: publish b7dcfee9-94e8-455b-baaf-d68f467315e4
ZeppelinSession: publish 513e39b4-5d7b-49c3-9131-9722abfa426a
Bokeh: BokehJS not loaded, scheduling load and callback at Sat Mar 11 2017 19:21:25 GMT+0100 (CET)
Bokeh: injecting script tag for BokehJS library:  https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.js
Bokeh: injecting script tag for BokehJS library:  https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.4.min.js
Bokeh: all BokehJS libraries loaded
Bokeh: BokehJS plotting callback run at Sat Mar 11 2017 19:21:25 GMT+0100 (CET)
[bokeh] setting log level to: 'info'
Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.css
Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.4.min.css
Bokeh: all callbacks have finished
```


## 4  Render a first plot

### 4.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark
opts = dict(plot_width=250, plot_height=250, min_border=0)
p1 = figure(**opts)
r1 = p1.circle([1,2,3], [4,5,6], size=20)

p2 = figure(**opts)
r2 = p2.circle([1,2,3], [4,5,6], size=20)

handle1 = show(row(p1, p2), notebook_handle=True)
```

### 4.2 Zeppelin Comm Layer Log File

```
2017-03-11 19:23:34,029 DEBUG:ZeppelinDisplayPublisher Publish html \n\n    <div class="bk-root">\n        <div class="bk-plotdiv" id="6faf5afc-cd81-4dee-9d34-340607fcce2b"></div>\n    </div>\n<script type="text/javascript">\n  \n  (function(global) {\n    function now() {\n      return new Date();\n    }\n  \n    var force = false;\n  \n    if (typeof (window._bokeh_onload_callbacks) === "undefined" || force === true) {\n      window._bokeh_onload_callbacks = [...(17177)]
2017-03-11 19:23:34,029 DEBUG:ZeppelinDisplayPublisher Delayed printing of <div id="0c8ea700-2e0b-4750-b332-a401289766b3"></div>
2017-03-11 19:23:34,067 INFO:ZeppelinComm New ZeppelinComm for target c2573fd0-002e-491d-b95e-699d40f8558f
2017-03-11 19:23:34,069 DEBUG:ZeppelinComm Register Comm 26d81593-4d7f-4dec-b1f1-826ad3f0651d with CommManager ...
2017-03-11 19:23:34,069 DEBUG:ZeppelinCommManager Registering comm 26d81593-4d7f-4dec-b1f1-826ad3f0651d
2017-03-11 19:23:34,069 DEBUG:ZeppelinComm ... and send comm_open for 26d81593-4d7f-4dec-b1f1-826ad3f0651d to notebook
```

### 4.3 Browser Web Console

```
Calling function __jupyterHandler with delay: 200
ZeppelinSession: publish 0c8ea700-2e0b-4750-b332-a401289766b3
Open comm for target_namec2573fd0-002e-491d-b95e-699d40f8558fand comm id 26d81593-4d7f-4dec-b1f1-826ad3f0651d
CommManager: new_comm target: c2573fd0-002e-491d-b95e-699d40f8558f comm_id: 26d81593-4d7f-4dec-b1f1-826ad3f0651d
Comm: Init
CommManager: register_comm comm_id: 26d81593-4d7f-4dec-b1f1-826ad3f0651d
CommManager: register_target: c2573fd0-002e-491d-b95e-699d40f8558f
Bokeh: BokehJS plotting callback run at Sat Mar 11 2017 19:23:34 GMT+0100 (CET)
[bokeh] Registering Jupyter comms for target c2573fd0-002e-491d-b95e-699d40f8558f
CommManager: register_target: c2573fd0-002e-491d-b95e-699d40f8558f
Bokeh: all callbacks have finished
Comm: on_msg
Comm: register_callback for msg      
```

