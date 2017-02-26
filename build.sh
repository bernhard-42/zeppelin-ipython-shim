mkdir -p jupytershim/js

uglifyjs jupytershim/js-src/comm.js \
         jupytershim/js-src/comm_manager.js \
         jupytershim/js-src/notebook_comm.js \
         jupytershim/js-src/kernel.js \
         jupytershim/js-src/notebook.js \
         -o jupytershim/js/jupyershim-min.js \
         --source-map jupytershim/js/jupyershim-min.js.map \
         -p 1
