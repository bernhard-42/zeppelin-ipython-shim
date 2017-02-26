## 1 Approach

### Rebuild the Jupyter/IPython display/comm system in Zeppelin. 

This involves 

- Creating a Comm and CommManager class in python for the interpreter and in javascript for the notebook
- Starting a small WebSocket based Forwarding server locally (neither in the python interpreter nor in the webbrowser a WebSocket Server can be started)
- Monkey Patching IPython (for displaying in Zeppelin) and ipykernel (for communicating via the new classes and the external WebSocket Server)

        from IPython.core.interactiveshell import InteractiveShell
        ip = InteractiveShell.instance()
        ip.display_pub = ZeppelinDisplayPublisher(self)
        
        import ipykernel.comm
        ipykernel.comm.Comm = ZeppelinComm
        ipykernel.comm.CommManager = ZeppelinCommManager
- Creating an Jupyter object in the browser necessary for the notebook communication part


### Class hierarchy:


```
Interpreter (Python) 								Notebook (Javascript)
--------------------                                ---------------------
JupyterShim 										Jupyter
NotebookComm										Notebook
Kernel												Kernel
CommManager											CommManager
Comm					<==>	WebSocket   <==>	Comm
								 Server
```

## 2 Supported Visualization libraries

### Bokeh (http://bokeh.pydata.org)

Supported features

- Display graphics inline

	```python
	output_notebook()
	```

- Interactively modify visualizations 

	```python
	push_notbook()
	```

- Bokeh Javascript Widgets interacting with the plot

As an example import [examples/JupyterShim Overview](examples/JupyterShim Overview.json) into Zeppelin

For some of the Bokeh Gallery plots see [examples/JupyterShim Bokeh Gallery](examples/JupyterShim Bokeh Gallery.json)


## 3 Usage

### Clone the project

```bash
cd /tmp
git clone https://github.com/bernhard-42/zeppelin-ipython-shim.git
```

### Start the local WebSockets based forwarding proxy

In the Terminal

```bash
pip install websocket-client websocket-server

cd zeppelin-ipython-shim/websocket-server/
python3 websocketServer.py
```


### Use the Shim

Ensure that the python module `websocket-client` is installed on the Zeppelin server machine

In Zeppelin Notebook

```python
import sys
sys.path += ["/tmp/zeppelin-ipython-shim"]

from jupytershim import JupyterShim
  
wsServer = "ws://<ws-server>:<port>"
j = JupyterShim(wsServer)
```


## 4 Limitations:

- ipywidgets don't work and will not work
- The shim only implements a one way communication from interpreter to notebook.
- currently tested with Bokeh 0.12.4 : all examples work with the following exceptions:
	- layout sizing_mode 'stretch_both' not working
	- mpl.toBokeh() not working
	- Bokeh server not covered


## 5 TODOs

- bokeh "layout" method: sizing_mode='stretch_both' function not working
- WebSocket Forward Proxy: Can it be moved to Zeppelin


## 6 Credits

As a shim for jupyter and ipython, the code in this project is based on the python modules

- [IPython](https://github.com/ipython/ipython): python display function ([license](https://github.com/ipython/ipython/blob/master/COPYING.rst))
- [Jupyter notebook](https://github.com/jupyter/notebook): javascript classes Comm and CommManager ([license](https://github.com/jupyter/notebook/blob/master/COPYING.md))
- [ipykernel](https://github.com/ipython/ipykernel): python classes Comm and CommManager ([license](https://github.com/ipython/ipykernel/blob/master/COPYING.md))

