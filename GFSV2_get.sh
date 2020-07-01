#!/bin/bash

docker-compose run --user 1000:1000 pygfsv2 python GFSV2_get.py --step 12 24 --level 700 850 --param tmp_pres --date 2005-01-01