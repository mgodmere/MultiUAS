#!/bin/bash
python scripts/generate_sitl.py $1
roslaunch launch/sitl_$1.launch
