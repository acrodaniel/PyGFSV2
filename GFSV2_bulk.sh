#!/bin/bash

docker-compose run -d --user 1000:1000 pygfsv2 python GFSV2_bulk.py --config spatialMOS.conf
