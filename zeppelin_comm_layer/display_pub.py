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

from IPython.core.displaypub import DisplayPublisher

class ZeppelinDisplayPublisher(DisplayPublisher):

    def __init__(self, zeppelinCommLayer):
        self.zeppelinCommLayer = zeppelinCommLayer
 
    def publish(self, data, metadata=None, source=None):
        doc = {}
        header = True
        for d in [data, metadata]:
            if isinstance(d, str):
                pass
            else:
                html = d.get("text/html")
                if html is not None: 
                    self.zeppelinCommLayer._print(html, header)
                    header = False
                    
                js = d.get("application/javascript")
                if js is not None: 
                    self.zeppelinCommLayer._printJs(js, header)
                    header = False
            
    def clear_output(self, wait=False):
        pass