
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

# Credits: http://stackoverflow.com/a/11927374

import os
import socket
import logging 
from .utils import Singleton
from six import with_metaclass


class LogLevel(with_metaclass(Singleton)):

    def setLogLevel(self, logLevel):
        self.logLevel = logLevel
        

class Logger(object):

    def __init__(self, name):
        logLevel = LogLevel().logLevel
        logger = logging.getLogger(name)
        logger.setLevel(logLevel)
        if not logger.handlers:
            log_dir = os.environ["ZEPPELIN_LOG_DIR"]
            prefix = "zeppelin-interpreter-pyspark-comm-layer"
            file_name = os.path.join(log_dir, '%s-%s-%s.log' % (prefix, os.environ["USERNAME"], socket.gethostname()))
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message).400s ...')
            handler.setFormatter(formatter)
            handler.setLevel(logLevel)
            logger.addHandler(handler)

        self._logger = logger

    def get(self):
        return self._logger
