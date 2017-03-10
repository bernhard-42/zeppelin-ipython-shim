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

from uuid import uuid4
from IPython.core.displaypub import DisplayPublisher
from .logger import Logger


class ZeppelinDisplayPublisher(DisplayPublisher):

    def __init__(self, kernel):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.propagate = False
        self.logger.info("New ZeppelinDisplayManager")
            
        self.kernel = kernel
 

    def publish(self, data, metadata=None, source=None):
        doc = {}
        header = True
        for d in [data, metadata]:
            if isinstance(d, str):
                pass
            else:
                html = d.get("text/html")
                if html is not None: 
                    self.logger.debug("Publish html %s" % html)
                    self.print(html, header)
                    header = False
                    
                js = d.get("application/javascript")
                if js is not None: 
                    self.logger.debug("Publish javascript %s" % js)
                    self.print('<script>' + js + '</script>', header)
                    header = False
            

    def print(self, html, header=False):
        div_id = str(uuid4())
        wrapper = '<div id="%s"></div>' % div_id
        self.logger.debug("Delayed printing of " + wrapper)
        if header:
            print("%angular")
        print(wrapper)
        self.kernel.send("publish", {"div_id":div_id, "html":html})
    
    
    def clear_output(self, wait=False):
        self.logger.debug("Clear output not implemented yet")
        pass
    
