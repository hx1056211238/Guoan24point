#!/bin/sh

LIUGH=`screen -ls`
RESULT=`echo $LIUGH |grep -c "web"`

if [ $RESULT -gt 0 ]; 
  then 

  echo "HF SYS is running"
  exit; 
fi

echo "running HF SYS...."

cd ~/hf_formation/run
screen -dmS ap python /home/pi/hf_formation/run_ap.py
screen -dmS net watch -n 60 python /home/pi/hf_formation/run_setnetwork.py
screen -dmS web bash /home/pi/hf_formation/run_webserver.sh
screen -dmS con python /home/pi/hf_formation/run/hf-main.py
