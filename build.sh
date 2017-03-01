mkdir -p zeppelin_comm_layer/js

uglifyjs zeppelin_comm_layer/js-src/comm.js \
         zeppelin_comm_layer/js-src/comm_manager.js \
         zeppelin_comm_layer/js-src/session.js \
         zeppelin_comm_layer/js-src/kernel.js \
         zeppelin_comm_layer/js-src/notebook.js \
         -o zeppelin_comm_layer/js/zeppelin_comm_layer-min.js \
         --source-map zeppelin_comm_layer/js/zeppelin_comm_layer-min.js.map \
         -p 1

