# Copyright 2017 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from six import with_metaclass
from zeppelin_comm_layer.utils import Singleton
from zeppelin_comm_layer.logger import Logger

from bokeh.core.state import State
from bokeh.document import Document
import bokeh.io


class BokehStates(with_metaclass(Singleton)):

    def __init__(self, zeppelinContext):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.propagate = False        
        self.logger.info("New BokehStates")
        self.zeppelinContext = zeppelinContext
        self._bokehStates = {}
        
        self.logger.info("Adding state to Bokeh output_notebook, show, push_notebook")
        bokeh.io.output_notebook = self.state_wrapper(bokeh.io.output_notebook, True)
        bokeh.io.show = self.state_wrapper(bokeh.io.show)
        bokeh.io.push_notebook = self.state_wrapper(bokeh.io.push_notebook, True)
        BokehStates.wrapperInitialized = True


    def initState(self):
        self.logger.info("Adding Bokeh state for notebook %s" % self.getNoteId())
        self._bokehStates[self.getNoteId()] = State()
        print("Bokeh is ready to be used")


    def getNoteId(self):
        return self.zeppelinContext.getInterpreterContext().getNoteId()


    def state_wrapper(self, func, proc=False):
        def func_wrapper(*args,**kwargs):
            bokeh.io._state = self._bokehStates[BokehStates().getNoteId()]
            result = func(*args,**kwargs)
            if not proc:
                return result
       
        return func_wrapper

