from IPython.core.displaypub import DisplayPublisher

class ZeppelinDisplayPublisher(DisplayPublisher):

    def __init__(self, jupyterShim):
        self.jupyterShim = jupyterShim
 
    def publish(self, data, metadata=None, source=None):
        doc = {}
        header = True
        for d in [data, metadata]:
            if isinstance(d, str):
                pass
            else:
                html = d.get("text/html")
                if html is not None: 
                    self.jupyterShim._print(html, header)
                    header = False
                    
                js = d.get("application/javascript")
                if js is not None: 
                    self.jupyterShim._printJs(js, header)
                    header = False
            
    def clear_output(self, wait=False):
        pass