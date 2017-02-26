## 1 Approach

### 1.1 Rebuild the Jupyter/IPython display/comm system in Zeppelin. 

This involves 

- Creating a Comm and CommManager class in python for the interpreter and in javascript for the notebook
- Monkey Patching IPython (for displaying in Zeppelin) and ipykernel (for communicating via the new classes and the external WebSocket Server)

        from IPython.core.interactiveshell import InteractiveShell
        ip = InteractiveShell.instance()
        ip.display_pub = ZeppelinDisplayPublisher(self)
        
        import ipykernel.comm
        ipykernel.comm.Comm = ZeppelinComm
        ipykernel.comm.CommManager = ZeppelinCommManager
- Creating an Jupyter object in the browser necessary for the notebook communication part


### 1.2 Object hierarchy:


```
Interpreter (Python) 								 		Notebook (Javascript)
--------------------                                 		---------------------
JupyterShim 										 		Jupyter
ZeppelinNotebookComm								 		Notebook
Kernel												 		Kernel
CommManager											 		CommManager
Comm					<==>	Zeppelin Angular   <==>		Comm
								  Backend API
```


## 2 Supported Visualization libraries

### 2.1 Bokeh (http://bokeh.pydata.org)

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


## 3 Installation

Clone the project

```bash
git clone https://github.com/bernhard-42/zeppelin-ipython-shim.git
```

Install the package 
```bash
cd /zeppelin-ipython-shim
pip install .
```

To compile the minified javascript library, install `uglifyjs`:

```bash
npm install uglify-js -g
```

and minify the javascript files

```bash
./build.sh
```


## 4 Usage

In Zeppelin Notebook

```python
from jupytershim import JupyterShim, resetJupyter

# To reset both the python JupyterShim singleton and the Javascript Jupyter object, 
# uncomment the next line
# resetJupyter()  

j = JupyterShim(z.z, debug=False)
```


## 5 Limitations:

- ipywidgets don't work and will not work
- The shim only implements a one way communication from interpreter to notebook.
- currently tested with Bokeh 0.12.4 : all examples work with the following exceptions:
	- layout sizing_mode 'stretch_both' not working
	- mpl.toBokeh() not working
	- Bokeh server not covered


## 6 Credits

As a shim für jupyter and ipython, the code in this project is based on the python modules

- [IPython](https://github.com/ipython/ipython): python display function ([license](https://github.com/ipython/ipython/blob/master/COPYING.rst))
- [Jupyter notebook](https://github.com/jupyter/notebook): javascript classes Comm and CommManager ([license](https://github.com/jupyter/notebook/blob/master/COPYING.md))
- [ipykernel](https://github.com/ipython/ipykernel): python classes Comm and CommManager ([license](https://github.com/ipython/ipykernel/blob/master/COPYING.md))

