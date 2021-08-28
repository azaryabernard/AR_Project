import speech_recognition as sr
import re
import philips_hue as ph
import pyaudio
import wave
import sh
from PyQt5.QtCore import pyqtSignal, QThread

r = sr.Recognizer()
m = sr.Microphone()

stopCommands = ["nevermind", "stop","stop listening"]
callCommand = ["star platinum", "star Platinum", "hey Google"]

volume = 50

def Record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME


def processCommand(speech):

    for stopCmd in stopCommands:
        if stopCmd in speech:
            print("stop listening...")
            return -1
    
#    forCommand = False
#    for cmd in callCommand:
#        if (cmd in speech):
#            print("call command specified")
#            forCommand = True
#            break
    
#    if not forCommand:
#        print("no command")
#        return -2
    

    lights_on = re.compile(r'^(?=.*turn)((?=.*lights)|(?=.*light))(?=.*on).*$', re.I)
    lights_off = re.compile(r'^(?=.*turn)((?=.*lights)|(?=.*light))(?=.*off).*$', re.I)
    decrease_brightness = re.compile(r'^(?=.*decrease)(?=.*brightness).*$', re.I)
    increase_brightness = re.compile(r'^(?=.*increase)(?=.*brightness).*$', re.I)
    set_brightness = re.compile(r'^(?=.*set)(?=.*brightness).*$', re.I)
    rotate_color = re.compile(r'^(?=.*rotate)((?=.*color)|(?=.*colour)).*$', re.I)
    set_color = re.compile(r'^(?=.*set)((?=.*color)|(?=.*colour)).*$', re.I)
    
    play_song = re.compile(r'^(?=.*play)*((?=.*song)|(?=.*something)).*$', re.I)
    stop_song = re.compile(r'^(?=.*stop)*((?=.*playing)|(?=.*music)).*$', re.I)
    pause_song = re.compile(r'^(?=.*pause)*((?=.*song)|(?=.*music)).*$', re.I)
    increase_volume = re.compile(r'^((?=.*increase)(?=.*volume))|((?=.*make)(?=.*louder)).*$', re.I)
    decrease_volume = re.compile(r'^((?=.*decrease)(?=.*volume))|((?=.*make)(?=.*softer)).*$', re.I)

    open_door = re.compile(r'^(?=.*open)(?=.*door).*$', re.I)
    close_door = re.compile(r'^(?=.*close)(?=.*door).*$', re.I)
    
    hand_tracking_on = re.compile(r'^(?=.*turn)(?=.*hand tracking)(?=.*on).*$', re.I)
    hand_tracking_off = re.compile(r'^(?=.*turn)(?=.*hand tracking)(?=.*off).*$', re.I)
    shut_down = re.compile(r'^((?=.*shutdown)|(?=.*shut down))(?=.*device).*$', re.I)

    if(hand_tracking_on.match(speech)):
        print("turning hand tracking on")
        return 1
    
    if(hand_tracking_off.match(speech)):
        print("turning hand tracking off")
        return 2
    
    if(shut_down.match(speech)):
        print("shutdown device")
        return 3

    if lights_on.match(speech):
        ph.turn_on_group('lights')
        print("turning lights on")
        return 0
    
    if lights_off.match(speech):
        ph.turn_off_group('lights')
        print("turning lights off")
        return 0
    
    if decrease_brightness.match(speech):
        ph.decrease_brightness_group('lights')
        print("decreasing brightness")
        return 0

    if increase_brightness.match(speech):
        ph.increase_brightness_group('lights')
        print("increasing brightness")
        return 0

    if set_brightness.match(speech):
        temp = re.findall(r'\d+', speech)
        percentage = list(map(int, temp))
        
        if percentage[0] > 100:
            ph.set_brightness_group('lights', 100)
            print("setting brightness to 100%")
        elif percentage[0] < 0:
            ph.set_brightness_group('lights', 0)
            print("setting brightness to 0%")
        else:
            ph.set_brightness_group('lights', percentage[0])
            print("setting brightness to " + str(percentage[0]) + "%")

        return 0

    if set_color.match(speech):
        temp = speech.split(" ")
        color = temp[-1]
        ph.set_color('lights', color)
        return 0

    if rotate_color.match(speech):
        ph.rotate_color()
        return 0

    if play_song.match(speech):
        print("playing a song")
        command_SoundSystem("Playing a song", volume, speech)
        return 0
    
    if stop_song.match(speech):
        print("stopping song")
        command_SoundSystem("Stopping song", volume, speech)
        return 0
    
    if pause_song.match(speech):
        print("pausing a song")
        command_SoundSystem("Pausing song", volume, speech)
        return 0

    if increase_volume.match(speech):
        print("increasing volume")
        edit_volume(10)
        command_SoundSystem("Increasing volume", volume, speech)
        return 0

    if decrease_volume.match(speech):
        print("decreasing volume")
        edit_volume(-10)
        command_SoundSystem("Decreasing volume", volume, speech)
        return 0
    
    if open_door.match(speech):
        print("opening door")
        command_Door('Open', speech)
        return 0
    
    if close_door.match(speech):
        print("closing door")
        command_Door('Closed', speech)
        return 0
    
    return -1


def edit_volume(vol):
    volume += vol

class ListenThread(QThread):
    command_signal = pyqtSignal(int, str)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True
        
    def run(self):
        try:
            print("A moment of silence, please...")
#             with m as source: r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            while self._run_flag:
                sh.cvlc('--play-and-exit', '../sound/sr_activation.m4a')
                print("Say something!")
                try :
                    with m as source: audio = r.listen(source, timeout = 3, phrase_time_limit = 5)
                except Exception as e:
                    print(e)
                    self.command_signal.emit(-1, "")
                    break

                print("Got it! Now to recognize it...")
                try:
                    # recognize speech using Google Speech Recognition
                    value = r.recognize_google(audio)

                    
                    print("You said {}".format(value))
                        
                    processed_command = processCommand(value)
                    self.command_signal.emit(processed_command, value)
                    break

                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                    self.command_signal.emit(-1, "")
                    break
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                    self.command_signal.emit(-1, "")
                    break
            
            
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
