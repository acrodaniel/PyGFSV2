#!/usr/bin/python
# -------------------------------------------------------------------
# - NAME:        download.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2017-08-04
# -------------------------------------------------------------------
# - DESCRIPTION: This python executable is used to download small
#                manually defined subsets of GFS reforecast v2 grib
#                files. For bulk downloads providing some more
#                settings please check the second executable
#                called GFSV2_bulk.
# -------------------------------------------------------------------
# - EDITORIAL:   2017-08-04, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2017-08-05 10:51 on thinkreto
# -------------------------------------------------------------------

import logging
import logging.config
import os
import time
from datetime import datetime

if not os.path.exists(os.path.join(os.getcwd(), "log")):
   os.mkdir(os.path.join(os.getcwd(), "log"))

starttime = datetime.now()
print(starttime)
logging_cfg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GFSV2/config/logging.conf")
logfile = os.path.join("log", f"logfile-{datetime.now().strftime('%Y-%m-%d')}.log")

logging.config.fileConfig(logging_cfg_file, disable_existing_loggers=False, defaults={"logfilename": logfile})
logging.Formatter.converter = time.localtime
logging.getLogger()

# -------------------------------------------------------------------
# Main part of the script
# -------------------------------------------------------------------
if __name__ == "__main__":

   # ----------------------------------------------------------------
   # Read config file now
   # ----------------------------------------------------------------
   import datetime as dt
   from GFSV2 import *

   # Checking user inputs
   inputs = inputCheck()

   # Read default config file
   config = readConfig()
   config.data = inputs.get("data")
   config.steps = inputs.get("steps")

   # Looping over dates
   for date in inputs.get("dates"):

      # Proccessing
      logging.info("Processing date {:s}".format(date.strftime("%Y-%m-%d %HZ")))

      download( config, date )
   logging.info("The program has run successfully")
