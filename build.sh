mkdir -p zeppelin_comm_layer/js

uglifyjs zeppelin_comm_layer/js-src/comm.js \
         zeppelin_comm_layer/js-src/comm_manager.js \
         zeppelin_comm_layer/js-src/session.js \
         zeppelin_comm_layer/js-src/kernel.js \
         zeppelin_comm_layer/js-src/notebook.js \
         zeppelin_comm_layer/js-src/main.js \
         -o zeppelin_comm_layer/js/zeppelin_comm_layer-min.js \
         -p 1

