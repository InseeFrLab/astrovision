#!/bin/bash
sudo apt-get update
sudo apt-get install python3-numpy -y
sudo apt-get install python3-gdal -y
sudo apt-get install libgdal-dev -y
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
