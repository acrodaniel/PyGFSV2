"""A class to create a logger"""

import logging
import logging.config
import os
import time
from datetime import datetime

class loggingmodule( object ):
    def __init__( self ):
        if not os.path.exists(os.path.join(os.getcwd(), "log")):
            os.mkdir(os.path.join(os.getcwd(), "log"))

        logging_cfg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/logging.conf")
        logfile = os.path.join("log", f"logfile-{datetime.now().strftime('%Y-%m-%d')}.log")

        logging.config.fileConfig(logging_cfg_file, disable_existing_loggers=False, defaults={"logfilename": logfile})
        logging.Formatter.converter = time.localtime
        logging.getLogger()