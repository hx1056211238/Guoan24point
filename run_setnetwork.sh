#!/bin/sh 
 sudo ifconfig eth0 192.168.125.22 netmask 255.255.255.0 
 sudo route add default gw 192.168.0.1
 sudo ifconfig eth0 up 
 
