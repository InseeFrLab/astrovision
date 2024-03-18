#!/bin/bash
mamba install -c conda-forge gdal=3.8.4 -y
export PROJ_LIB=/opt/mamba/share/proj
