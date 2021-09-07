import os
import sh
from time import time, sleep
from _config import *

winids = []

def searchWinID(appname):
    timeout = time() + 10
    while True:
        sleep(.1)
        if time() > timeout:
            print("ERROR EMBED APP")
            return False, -1
        try:    
            winid = int([l for l in sh.xwininfo('-root','-tree').split('\n') if appname in l][0].split('"' + appname)[0].strip(), 16)
        except:
            continue
        else:
            break
    return True, winid

os.system('DISPLAY=:0 xrandr --output HDMI-1 --rotate right')
os.system('DISPLAY=:0 xrandr -x')
os.system('lxterminal --command="python3 /home/pi/AR_Project/src/main.py"')

ret, winid = searchWinID('AR Prototype')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
winids.append(winid)

#START VNC SERVER
os.system('lxterminal --command="x11vnc -id {}"'.format(winid))
sleep(1)
os.system('lxterminal --command="vncviewer localhost:5900 -AutoReconnect=0 -AuthCertificate=0 -UseLocalCursor=0 -ClientCutText=0 -DotWhenNoCursor -EnableChat=0 -EnableToolbar=0 -RelativePtr=0 -Scaling 100% -SendKeyEvents=0 -SendPointerEvents=0 -ServerCutText=0 -ShareFiles=0 -SingleSignOn=0" ')
sleep(1)

ret, winid = searchWinID('localhost:5900 (')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
winids.append(winid)
#sh.xrandr('-x')
os.system('DISPLAY=:0 xdotool windowmove {} {} {} {}'.format('--', winids[1], OFFSET_X2,  OFFSET_Y2))
os.system('DISPLAY=:0 xdotool windowmove {} {} {} {}'.format('--', winids[0], OFFSET_X1,  OFFSET_Y1))
os.system('DISPLAY=:0 xdotool windowactivate {}'.format(winids[0]))

for appname in ['vncviewer": ("', 'python3": ("', 'x11vnc": ("' , 'pi@raspberrypi: ~/AR_Project/src": ("']:
    ret, winid = searchWinID(appname)
    if not ret:
        continue
    sh.xdotool('windowminimize', winid)

