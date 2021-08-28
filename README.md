# AR_Project
Personal augmented reality project for my DIY AR-glasses (Raspberry Pi 4)

1. mediapipe and opencv (only works for python3.7 with pip3 as (python3.7 -m pip install)):

pip3 install -U numpy

sudo apt install ffmpeg python3-opencv

sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23

sudo pip3 install mediapipe-rpi4


2. PyQt5 and PyQt5.QtWebEngine:

sudo apt-get install python3-pyqt5

sudo apt install aptitude

sudo echo "deb [trusted=yes]  http://deb.debian.org/debian/ oldstable main contrib non-free" >> /etc/apt/sources.list

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys <SECOND KEY IN ERROR MESSAGE> 

sudo apt update && sudo apt-get update (in somecase may need --allow-unauthenticated)

sudo aptitude install python3-pyqt5.qtwebengine (1. option: NO (n), 2.option: YES (y))

sudo nano /etc/apt/sources.list and comment the newly added oldstable repository for safety reasons


3. speechrecognition:

pip3 install speechrecognition

sudo apt-get install portaudio19-dev

sudo apt-get install python3-all-dev

sudo apt-get install python3-pyaudio
  
sudo pip3 install adafruit-python-shell
  
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
  
sudo python3 i2smic.py
  
sudo apt install xdotool  
  
sudo apt-get install flac  
  

4. vnc for screen mirroring (I can't get dual split screen with screen mirror working):

sudo apt install x11vnc

sudo apt-get install realvnc-vnc-viewer
  

5. etc:

pip3 install sh

pip3 install rgbxy

pip3 install webcolors

pip3 install pynput
