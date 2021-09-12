import os
import sys
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
            winid = int([l for l in sh.xwininfo('-root', '-tree').split('\n') if appname in l][0].split('"' + appname)[0].strip(), 16)
        except:
            continue
        else:
            break
    return True, winid

os.system('xrandr --output HDMI-1 --rotate right')
os.system('xrandr -x')
os.system('''lxterminal --title="pi@raspberrypi: ~/AR_Project/src" --command="/bin/sh -c 'python3 main.py 2>&1 main.log'"''')
ret, winid = searchWinID('AR Prototype')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
winids.append(winid)

#START VNC SERVER
port = 5900
if len(sys.argv) > 1:
    port = sys.argv[1]
print(f'opening x11vnc at port: {port}')
os.system(f"lxterminal --command='x11vnc -id {winid} -rfbport {port}'")
sleep(1)
os.system(f'lxterminal --command="vncviewer localhost:{port} -AutoReconnect=0 -AuthCertificate=0 -ClientCutText=0 -DotWhenNoCursor -EnableChat=0 -EnableToolbar=0 -RelativePtr=0 -Scaling 100% -SendKeyEvents=0 -SendPointerEvents=1 -ServerCutText=0 -ShareFiles=0 -SingleSignOn=0" ')
sleep(1)

ret, winid = searchWinID(f'localhost:{port} (')

if not ret:
    print('error getting winID')
    quit()

print(winid)
sleep(1)
winids.append(winid)
#sh.xrandr('-x')
os.system('xdotool windowmove {} {} {} {}'.format('--', winids[1], OFFSET_X2,  OFFSET_Y2))
os.system('xdotool windowmove {} {} {} {}'.format('--', winids[0], OFFSET_X1,  OFFSET_Y1))
os.system('xdotool windowactivate {}'.format(winids[0]))

for appname in ['vncviewer": ("', 'python3": ("', 'x11vnc": ("' , 'pi@raspberrypi: ~/AR_Project/src": ("']:
    ret, winid = searchWinID(appname)
    if not ret:
        continue
    os.system(f'xdotool windowminimize {winid}')

