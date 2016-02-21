#!/bin/bash
sudo modprobe bcm2835-v4l2
export LD_LIBRARY_PATH=/home/pi/dev/git/RemoteBotServer/mjpg-experimental/mjpg-streamer/mjpg-streamer-experimental
cd /home/pi/dev/git/RemoteBotServer/mjpg-experimental/mjpg-streamer/mjpg-streamer-experimental
/home/pi/dev/git/RemoteBotServer/mjpg-experimental/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "input_raspicam.so -fps 30 -x 320 -y 240 -hf -vf" -o "./output_http.so -w ./www"
