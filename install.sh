#!/bin/bash 

OPTSTRING=":i"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    i) 
       # Handle the -i flag
       # Update dependencies
       echo "Install Luma.core drivers"
       apt update --fix-missing
       apt install python3.7-dev python3-pip libfreetype6-dev libjpeg-dev dsniff mitmproxy -y
       pip3 install --upgrade luma.oled
       pip3 install --upgrade luma.lcd
       pip3 install --upgrade luma.core
       ;;
    \?) 
       # Handle invalid flags
       ;;
  esac
done

echo "Create directories"
mkdir -p /root/BeBoXGui/{images,nmap}
echo "Copying files"
cp *.py /root/BeBoXGui/
cp images/* /root/BeBoXGui/images/

echo "Copying scripts in local P4wnP1 script"
cp scripts/runmenu.sh /usr/local/P4wnP1/scripts/
chmod +x /usr/local/P4wnP1/scripts/runmenu.sh
cp scripts/startReverseShellListener.sh /usr/local/P4wnP1/scripts/
chmod +x /usr/local/P4wnP1/scripts/startReverseShellListener.sh

echo "Copying HIDscripts in local P4wnP1"
cp HIDscripts/*.js /usr/local/P4wnP1/HIDScripts/

echo "Copying helper in local P4wnP1"
cp helper/* /usr/local/P4wnP1/helper/

cp update.sh /root/BeBoXGui/
chmod +x /root/BeBoXGui/update.sh
echo "All files are ready"
echo "to run with P4wnP1 boot"
echo "Go thru web interface"
echo "Go in trigger section"
echo "Create new trigger"
echo "on service start :"
echo "run script sh and choose "
echo "runmenu.sh"
echo "Enjoy"
echo "by default gui.py use SPI interface"
echo "if you use I2C oled edit gui.py"
echo "and set I2C_USER = 1"
echo "Run this to init usb storage:"
echo "cd /usr/local/P4wnP1/helper"
echo "bash genimg -i RoboLoader -o RoboLoader -s 1000"

