#!/usr/bin/env bash

# Before running this file do the following on the raspbery pi
# Add git and your git info
# sudo apt -y install git
# git config --global user.name "iot"
# git config --global user.email ""
# git clone https://github.com/somervda/iot.git



# Make sure apt is updated and we have the latest package lists before we start
# Remember to 'sudo chmod u+x setup.sh' to be able to run this script 
# then 'bash setup.sh'

date
echo 1. Updating and Upgrade apt packages 
sudo apt update -y
sudo apt upgrade -y

echo 2. Installing and rationalizing Python Version Names
sudo apt install -y python-is-python3
sudo apt install -y python3-pip
sudo apt install -y python-dev-is-python3

python --version
pip --version

# Create postgresql environment see https://pimylifeup.com/raspberry-pi-postgresql/ 
echo 3. Install postgresql
sudo apt install postgresql -y
# add the pi user as a postgresql user
sudo su postgres
createuser pi -P --interactive
# Note: this is interactive , you will need to set a postgress password for user pi 
# and make pi an administrative user
# Once the createuser command has completed then run 
# psql
# CREATE DATABASE pi;
# exit
# and 
# exit again to return to a pi session

# finally run the following to create the ioydb
# psql
# \i iot.sql

# Install the python postgresql client library
# Note: Use sudo rm /usr/lib/python3.*/EXTERNALLY-MANAGED
#       to remove the python --break-system-package requirement
pip install psycopg --break-system-package



