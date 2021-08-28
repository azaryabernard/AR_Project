import os
import sh
from time import time, sleep
from _config import *

def searchWinID(appname):
    timeout = time() + 10
    while True:
        sleep(.1)
        if time() > timeout:
            print("ERROR EMBED APP")
            return False, -1
        try:    
            winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if appname in l][0].split('"' + appname)[0].strip(), 16)
        except:
            continue
        else:
            break
    return True, winid

sh.xrandr('--output','HDMI-1','--rotate', 'left')
sh.xrandr('-x')
os.system('lxterminal --command="python3 /home/pi/AR_Project/src/main.py"')

ret, winid = searchWinID('AR Prototype')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
sh.xdotool('windowmove', winid, OFFSET_X1, OFFSET_Y1)
#START VNC SERVER
os.system('lxterminal --command="x11vnc -id {}"'.format(winid))
sleep(1)
os.system('lxterminal --command="vncviewer localhost:5900 -AutoReconnect=0 -AuthCertificate=0 -ClientCutText=0 -DotWhenNoCursor -EnableChat=0 -EnableToolbar=0 -RelativePtr=0 -Scaling 100% -SendKeyEvents=0 -SendPointerEvents=0 -ServerCutText=0 -ShareFiles=0 -SingleSignOn=0"')
sleep(1)

ret, winid = searchWinID('localhost:5900 (')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
sh.xdotool('windowmove', winid, OFFSET_X2, OFFSET_Y2)
#sh.xrandr('-x')

for appname in ['vncviewer": ("lxterminal"', 'python3": ("lxterminal"', 'x11vnc": ("lxterminal"' , 'pi@raspberrypi: ~/AR_Project/src": ("lxterminal"']:
    ret, winid = searchWinID(appname)
    if not ret:
        continue
    sh.xdotool('windowminimize', winid)