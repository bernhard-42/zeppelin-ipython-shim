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

from zeppelin_comm_layer.logger import Logger

class VegaLite:
    def __init__(self, session):
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.propagate = False        
        self.logger.info("New BokehStates")

        self.session = session

        print("""%html
        <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
        <script src="http://vega.github.io/vega/vega.js" charset="utf-8"></script>
        <script src="http://vega.github.io/vega-lite/vega-lite.js" charset="utf-8"></script>
        <div>Execute <vg>.output_notebook() in the next paragraph (<vg> references the VegaLite instance)</div>
        """)
        
    def output_notebook(self):
        self.logger.info("Redirecting output to Zeppelin Notebook")
        jsFunc = """
        vgplot = function(session, object) {
            var embedSpec = {
              mode: "vega-lite",
              spec: object.vlSpec
            }
            console.log(object)
            setTimeout(function(){ 
                var divId = "__vgplot_" + object.plotId + "__";
                var titleDivId = "__vgplot_" + object.plotId + "_title__";
                
                if (object.height > 0) {
                    document.getElementById(divId).setAttribute("style","height:" + object.height + "px");
                }
                document.getElementById(titleDivId).innerHTML = "<span style='font-size: 60%; color: #aaa'>plotId= " + object.plotId + "</span>";
                if (object.title != "") {
                    document.getElementById(titleDivId).innerHTML += "<h4>" + object.title + "</h4>";
                }
                vg.embed("#" + divId, embedSpec, function(error, result) {
                    console.log("Plot " + object.plotId + " finished")
                });
            }, object.delay);
        }
        """
        self.session.registerFunction("vgplot", jsFunc)

        print("""%html
        <script src="http://vega.github.io/vega-editor/vendor/vega-embed.js" charset="utf-8"></script>
        <div>Vega-Lite is ready to be used</div>
        """)
        
    def plot(self, plotId, vlSpec, title="", delay=200, height=None):
        self.logger.debug("Plotting %s" % plotId)
        self.prepare(plotId)
        self.update(plotId, vlSpec, title, delay, height)

    def prepare(self, plotId):
        self.logger.debug("Preparing %s" % plotId)
        print("%angular")
        print("""
        <div id="__vgplot_%s_title__"></div>
        <div id="__vgplot_%s__"></div>
        """ % (plotId, plotId))
        
    def update(self, plotId, vlSpec, title="", delay=200, height=None):
        self.logger.debug("Updating %s" % plotId)
        if height is None:
            height = -1
        else:
            height = height + 100
        self.session.call("vgplot", {"plotId":plotId, "vlSpec":vlSpec, "delay":delay, "height":height, "title":title})
 
    def dfToJson(self, df, columns):
        return [dict([(col, row[1][col]) for col in columns])  for row in list(df.iterrows())]
    