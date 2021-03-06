#!/bin/bash

# general
sudo apt-get -y install cmake python python-pip

# ros
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get -y update
sudo apt-get -y install ros-melodic-desktop-full
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
sudo apt-get -y install python-rosinstall python-rosinstall-generator python-wstool build-essential
sudo pip install jinja2 numpy toml

# PX4 SITL
cd Firmware
git submodule init
git submodule update
make posix_sitl_default
make posix_sitl_default sitl_gazebo
echo "source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/posix_sitl_default" >> ~/.bashrc
echo "ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd):$(pwd)/Tools/sitl_gazebo" >> ~/.bashrc
source ~/.bashrc
cd ..

# dronekit
sudo pip install dronekit
