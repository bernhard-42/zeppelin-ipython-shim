## 1 Import the Zeppelin Comm Layer, intialize it ...

### 1.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark

from zeppelin_comm_layer import ZeppelinCommLayer

zcl = ZeppelinCommLayer(z.z, logLevel="DEBUG")
```

### 1.2 Zeppelin Comm Layer Log File

```
2017-03-03 18:07:09,038 INFO:ZeppelinCommLayer Initializing ZeppelinCommLayer singleton
2017-03-03 18:07:09,038 DEBUG:ZeppelinCommLayer Patching ipykernel Comm and CommManager
2017-03-03 18:07:09,038 INFO:ZeppelinSession New ZeppelinSession
2017-03-03 18:07:09,038 DEBUG:ZeppelinCommLayer Patching InteractiveShell.kernel
2017-03-03 18:07:09,038 DEBUG:ZeppelinCommLayer Setting IPython Display Manager
2017-03-03 18:07:09,038 INFO:ZeppelinDisplayPublisher New ZeppelinDisplayManager
2017-03-03 18:07:09,039 DEBUG:ZeppelinSession Reset $scope.____zeppelin_comm_NoteId=2C9HR8ADP_msg__
2017-03-03 18:07:09,040 INFO:ZeppelinSession Loading Comm Layer Javascript libs```
```

### 1.3 Browser Web Console

```
Comm Layer Javascript libs loaded                                                   localhost:8080:3:1
```


## 2 ... and start it in the next (!) Zeppelin paragraph

### 2.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark

zcl.start()
```

### 2.2 Zeppelin Comm Layer Log File

```
2017-03-03 18:09:08,630 INFO:ZeppelinCommLayer Starting Comm Layer Watcher
2017-03-03 18:09:08,631 DEBUG:ZeppelinSession Starting Angular watcher for $scope.____zeppelin_comm_2C9HR8ADP_msg__
```

### 2.3 Browser Web Console

```
Get scope for div id__Zeppelin_Session_2C9HR8ADP_Comm__                             localhost:8080:10:9
NoteboooComm: Cancel watchers                                                       localhost:8080:14:13
Initiate Javascript Notebook Comms for divId __Zeppelin_Session_2C9HR8ADP_Comm__    localhost:8080:22:9
Notebook: init                                                                      localhost:8080:1:4793
Kernel: init                                                                        localhost:8080:1:4507
ZeppelinSession: init                                                               localhost:8080:1:2953
CommManager: Init                                                                   localhost:8080:1:1371
Install Angular watcher for session comm var ____zeppelin_comm_2C9HR8ADP_msg__      localhost:8080:26:9
Angular script already executed, skipped                                            localhost:8080:38:9
```


## 3 Adapt Bokeh global state management to Zeppelin

### 3.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark

zcl.enableBokeh()
```

### 3.2 Zeppelin Comm Layer Log File
```
2017-03-03 18:13:36,866 INFO:BokehStates Adding Bokeh state for notebook 2C9HR8ADP
```

### 3.3 Browser Web Console

n/a


## 4 Load Bokeh libraries and redirect output to Zeppelin Notebook

### 4.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.resources import Resources
from bokeh.plotting import figure

output_notebook()
```

### 4.2 Zeppelin Comm Layer Log File

```
2017-03-03 18:14:35,145 DEBUG:ZeppelinDisplayPublisher Publish html \n    <div class="bk-root">\n        <a href="http://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>\n        <span id="5d890ee3-7421-4247-9bac-0070db397bdf">Loading BokehJS ...</span>\n    </div>
2017-03-03 18:14:35,147 DEBUG:ZeppelinSession Delayed printing of <div id="0d2fc49b-8f76-4b36-90d5-d27a4d0530ce"></div>
2017-03-03 18:14:35,148 DEBUG:ZeppelinSession Sending task publish to $scope.____zeppelin_comm_2C9HR8ADP_msg__ for message {'html': '\n    <div class="bk-root">\n        <a href="http://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>\n        <span id="5d890ee3-7421-4247-9bac-0070db397bdf">Loading BokehJS ...</span>\n    </div>', 'div_id': '0d2fc49b-8f76-4b36-90d5-d27a4d0530ce'}
2017-03-03 18:14:35,150 DEBUG:ZeppelinDisplayPublisher Publish javascript \n(function(global) {\n  function now() {\n    return new Date();\n  }\n\n  var force = "1";\n\n  if (typeof (window._bokeh_onload_callbacks) === "undefined" || force !== "") {\n    window._bokeh_onload_callbacks = [];\n    window._bokeh_is_loading = undefined;\n  }\n\n\n  \n  if (typeof (window._bokeh_timeout) === "undefined" || force !== "") {\n    window._bokeh_timeout = Date.now() + 5 [...(4363)]
2017-03-03 18:14:35,152 DEBUG:ZeppelinSession Delayed printing of <div id="02afa5e9-1270-4172-bfac-7e80515a35c3"></div>
2017-03-03 18:14:35,153 DEBUG:ZeppelinSession Sending task publish to $scope.____zeppelin_comm_2C9HR8ADP_msg__ for message {'html': '<script>\n(function(global) {\n  function now() {\n    return new Date();\n  }\n\n  var force = "1";\n\n  if (typeof (window._bokeh_onload_callbacks) === "undefined" || force !== "") {\n    window._bokeh_onload_callbacks = [];\n    window._bokeh_is_loading = undefined;\n  }\n\n\n  \n  if (typeof (window._b [...(4664)]
```

### 4.3 Browser Web Console

```
Angular script already executed, skipped                                                                               localhost:8080:38:9
ZeppelinSession: publish 0d2fc49b-8f76-4b36-90d5-d27a4d0530ce                                                          localhost:8080:1:4150
ZeppelinSession: publish 02afa5e9-1270-4172-bfac-7e80515a35c3                                                          localhost:8080:1:4150
Bokeh: BokehJS not loaded, scheduling load and callback at Date 2017-03-03T17:14:35.595Z                               localhost:8080:61:5
Bokeh: injecting script tag for BokehJS library:  "https://cdn.pydata.org/bokeh/release/bokeh-0.12.2.min.js"           localhost:8080:78:7
Bokeh: injecting script tag for BokehJS library:  "https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.2.min.js"   localhost:8080:78:7
Bokeh: injecting script tag for BokehJS library:  "https://cdn.pydata.org/bokeh/release/bokeh-compiler-0.12.2.min.js"  localhost:8080:78:7
Bokeh: all BokehJS libraries loaded                                                                                    localhost:8080:71:11
Bokeh: BokehJS plotting callback run at Date 2017-03-03T17:14:35.927Z                                                  localhost:8080:130:7
Bokeh: setting log level to: 'info'                                                                                    bokeh-0.12.2.min.js:2:25032
"Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-0.12.2.min.css"                                      localhost:8080:99:7
"Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.2.min.css"                              localhost:8080:101:7
Bokeh: all callbacks have finished                                                                                     localhost:8080:48:5
```


## 5  Render a first plot

### 5.1 Zeppelin Notebook (NoteId=2C9HR8ADP)

```python
%pyspark
opts = dict(plot_width=250, plot_height=250, min_border=0)
p1 = figure(**opts)
r1 = p1.circle([1,2,3], [4,5,6], size=20)

p2 = figure(**opts)
r2 = p2.circle([1,2,3], [4,5,6], size=20)

handle1 = show(row(p1, p2), notebook_handle=True)
```

### 5.2 Zeppelin Comm Layer Log File

```
2017-03-03 18:23:34,498 DEBUG:ZeppelinDisplayPublisher Publish html \n\n    <div class="bk-root">\n        <div class="plotdiv" id="738bad8c-37a7-4c12-a5f7-03847097ad65"></div>\n    </div>\n<script type="text/javascript">\n  \n  (function(global) {\n    function now() {\n      return new Date();\n    }\n  \n    var force = "";\n  \n    if (typeof (window._bokeh_onload_callbacks) === "undefined" || force !== "") {\n      window._bokeh_onload_callbacks = [];\n    [...(16954)]
2017-03-03 18:23:34,500 DEBUG:ZeppelinSession Delayed printing of <div id="1e0c6c1c-d716-4aae-b5da-6da2eff5e7a3"></div>
2017-03-03 18:23:34,501 DEBUG:ZeppelinSession Sending task publish to $scope.____zeppelin_comm_2C9HR8ADP_msg__ for message {'html': '\n\n    <div class="bk-root">\n        <div class="plotdiv" id="738bad8c-37a7-4c12-a5f7-03847097ad65"></div>\n    </div>\n<script type="text/javascript">\n  \n  (function(global) {\n    function now() {\n      return new Date();\n    }\n  \n    var force = "";\n  \n    if (typeof (window._bokeh_onload_call [...(17244)]
2017-03-03 18:23:34,504 INFO:ZeppelinComm New ZeppelinComm for target 84ce1a2a-f1f8-4956-8eae-9a468deccba6
2017-03-03 18:23:34,504 DEBUG:ZeppelinComm Register Comm 1c90308f-fc70-426d-b7e2-39c0475ce95e with CommManager ...
2017-03-03 18:23:34,505 DEBUG:ZeppelinCommManager Registering comm 1c90308f-fc70-426d-b7e2-39c0475ce95e
2017-03-03 18:23:34,505 DEBUG:ZeppelinComm ... and send comm_open for 1c90308f-fc70-426d-b7e2-39c0475ce95e to notebook
2017-03-03 18:23:34,505 DEBUG:ZeppelinSession Sending task comm_open to $scope.____zeppelin_comm_2C9HR8ADP_msg__ for message {'comm_id': '1c90308f-fc70-426d-b7e2-39c0475ce95e', 'target_name': '84ce1a2a-f1f8-4956-8eae-9a468deccba6', 'data': {}, 'metadata': None}
```

### 5.3 Browser Web Console

```
ZeppelinSession: publish 1e0c6c1c-d716-4aae-b5da-6da2eff5e7a3                                                     localhost:8080:1:4150
Open comm for target_name84ce1a2a-f1f8-4956-8eae-9a468deccba6and comm id 1c90308f-fc70-426d-b7e2-39c0475ce95e     localhost:8080:1:3461
CommManager: new_comm target: 84ce1a2a-f1f8-4956-8eae-9a468deccba6 comm_id: 1c90308f-fc70-426d-b7e2-39c0475ce95e  localhost:8080:1:1656
Comm: Init                                                                                                        localhost:8080:1:42
CommManager: register_comm comm_id: 1c90308f-fc70-426d-b7e2-39c0475ce95e                                          localhost:8080:1:2241
CommManager: register_target: 84ce1a2a-f1f8-4956-8eae-9a468deccba6                                                localhost:8080:1:1943
Bokeh: BokehJS plotting callback run at Date 2017-03-03T17:23:34.923Z                                             localhost:8080:130:9
Bokeh: Registering Jupyter comms for target 84ce1a2a-f1f8-4956-8eae-9a468deccba6                                  bokeh-0.12.2.min.js:71:4825
CommManager: register_target: 84ce1a2a-f1f8-4956-8eae-9a468deccba6                                                localhost:8080:1:1943
Bokeh: all callbacks have finished                                                                                localhost:8080:52:7
Comm: on_msg                                                                                                      localhost:8080:1:723
Comm: register_callback for msg                                                                                   localhost:8080:1:597

        
```

