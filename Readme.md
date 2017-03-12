# Jupyter/IPython display shim for Apache Zeppelin

## 1 Overview

Some visualisation libraries for Python can plot directly in Jupyter/IPython notebooks. These libraries rely e.g. on:

1. matplotlib
2. Jupyter/IPython display and communication system
3. ipywidgets

[Apache Zeppelin](http://zeppelin.apache.org/) version 0.7.0+ will support plotting matplotlib inline. However, it is not compatible with option 2 and 3.

This project creates a shim in [Apache Zeppelin](http://zeppelin.apache.org/) that simulates option 2, but does not cover option 3. It is based on the advanced Angular capabilities for Zeppelin ([ZeppelinSession](https://github.com/bernhard-42/advanced-angular-for-pyspark)).

As an example it uses Bokeh 0.12.4+ to visualise (`output_notebook`) or modify (`push_notebook`) plots inline in [Apache Zeppelin](http://zeppelin.apache.org/).
 
Tested with Python 2.7 (Ubuntu 16.10) and Python 3.5 (as of Anaconda3 4.2).


## 2 Installation

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



## 3 Usage

In Zeppelin Notebook

```python
%pyspark

from zeppelin_comm_layer import ZeppelinCommLayer, resetZeppelinCommLayer, LogLevel

# resetZeppelinCommLayer(z.z)
LogLevel().setLogLevel("DEBUG")

zcl = ZeppelinCommLayer(z.z)
```

In the next Paragraph start the shim (note: this cannot be done in the paragraph above)

```bash
zcl.start()
```


## 4 Test with Bokeh (http://bokeh.pydata.org)

**Note:** Bokeh global state management depends on a global variable which is sufficient if there is a 1-to-1 relationship between a notebook and a kernel as with IPython. Zeppelin will have multiple notebooks for each interpreter, hence Bokeh state management needs to be enhanced to support a state per Zeppelin Notebook (else `push_notebook`will fail when more than one tab with notebooks and Bokeh plots are open). For a solution look at [Zeppelin Visualizations](https://github.com/bernhard-42/zeppelin-visualizations)

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

As an example view [ZeppelinCommLayer Overview.md](notebooks/ZeppelinCommLayer Overview.md) or import [notebooks/ZeppelinCommLayer Overview.json](notebooks/ZeppelinCommLayer Overview.json) into Zeppelin

For some of the Bokeh Gallery plots see [ZeppelinCommLayer Bokeh Gallery.md](notebooks/ZeppelinCommLayer Bokeh Gallery.md) or import [notebooks/ZeppelinCommLayer Bokeh Gallery.json](notebooks/ZeppelinCommLayer Bokeh Gallery.json)


## 5 Limitations:

- The shim only implements a one way communication from interpreter to notebook.
- currently tested with Bokeh 0.12.4: all examples work with the following exceptions:
  - layout sizing_mode 'stretch_both' not working
  - mpl.toBokeh() not working
  - Bokeh server not covered
- *ipywidgets* don't work and might never work



## 6 Approach

### 6.1 Simulate the Jupyter/IPython display and communication system in Zeppelin. 

This involves 

- Creating a *Comm* and *CommManager* class in python for the interpreter and in javascript for the notebook
- Monkey Patching *IPython* (for displaying in Zeppelin) and *ipykernel* (for communicating via the new classes and the Zeppelin Angular Backend API)

  ```python
  from IPython.core.interactiveshell import InteractiveShell
  ip = InteractiveShell.instance()
  ip.display_pub = ZeppelinDisplayPublisher(self.kernel)

  import ipykernel.comm
  ipykernel.comm.Comm = ZeppelinComm
  ipykernel.comm.CommManager = ZeppelinCommManager
  ```
- Creating an Jupyter object in the browser necessary for the notebook communication part


### 6.2 Object hierarchy:

```
   Interpreter (Python)                                     Notebook (Javascript)
   --------------------                                     ---------------------

   ZeppelinCommLayer (N)                                          Jupyter
          v                                                          v
IPython InteractiveShell (S)                                     Notebook
          v                                                          v 
        Kernel                                                     Kernel
          v                                                          v
    ZeppelinSession         <==>    Zeppelin Angular   <==>    ZeppelinSession
    CommManager (S)                   Backend API                CommManager  
          ^                                                          ^
     ZeppelinComm                                                  Comm


(N) = Single Instance per Zeppelin Notebook
(S) = Singleton
```

### 6.3 Startup Phase

[Startup.md](Startup.md) shows per Notebook Paragraph (as in [notebooks/ZeppelinCommLayer Overview](examples/ZeppelinCommLayer Overview.json)):

- Zeppelin notebook inputs 
- Zeppelin Comm Layer log file per
- Browser Web Console output



## 7 Credits

As a shim for jupyter and ipython, the code in this project is based on the python modules

- [IPython](https://github.com/ipython/ipython): python display function (=> [license](https://github.com/ipython/ipython/blob/master/COPYING.rst))
- [Jupyter notebook](https://github.com/jupyter/notebook): javascript classes Comm and CommManager (=> [license](https://github.com/jupyter/notebook/blob/master/COPYING.md))
- [ipykernel](https://github.com/ipython/ipykernel): python classes Comm and CommManager (=> [license](https://github.com/ipython/ipykernel/blob/master/COPYING.md))



## 8 License

Copyright 2017 Bernhard Walter

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


