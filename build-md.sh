#!/bin/bash

filename="${1%.*}"
zeppelin2md "$1" "$(basename $(pwd))" -o "${filename}.md"


# convert ~/Downloads/bokeh_plot.png ~/Downloads/bokeh_plot\(1\).png +append bokeh-overview-1.2.png
# convert -delay 100 -loop 0 bokeh2*.png bokeh-overview-2.gif
# convert ~/Downloads/bokeh_plot.png ~/Downloads/bokeh_plot\(1\).png ~/Downloads/bokeh_plot\(2\).png +append bokeh-overview-3.png
# convert ~/Downloads/bokeh_plot\(2\).png ~/Downloads/bokeh_plot\(1\).png ~/Downloads/bokeh_plot.png +append bokeh-overview-4.png
# convert  ~/Downloads/bokeh_plot\(4\).png ~/Downloads/bokeh_plot\(3\).png +append bokeh-overview-5.png
# convert  -delay 100 -loop 0  bokeh6.* bokeh-overview-6.gif
# convert -background white -alpha remove vega1.3.png vega1.3-w.png