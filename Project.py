
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('sia', 'see', 'siaa', 'sai', 'cia'),
    "tbr": ('tell', 'what', 'show', 'how', 'me', 'Sia', 'sia', 'cia'),
    "cmds": {
        "ctime": ('time', 'current time', 'what time is it', 'give me the current time'),
        "radio": ('turn on the music', 'turn on the radio', 'music', 'radio'),
        "stupid1": ('tell me the joke', 'joke', 'make me laugh', 'laugh')
    }
}


# functions
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="en-US").lower()
        print("[log] Identified: " + voice)

        if voice.startswith(opts["alias"]):
            # speaking with sia
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # recognizing a command and executing it
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] I'm sorry I couldn't get you")
    except sr.RequestError as e:
        print("[log] Unknown error, please check the internet.")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        speak("It's " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # turning radio
        os.system("D:\\Temur\\music mp3\\04_-_Sia_-_Move_Your_Body.mp3")

    elif cmd == 'stupid1':
        # jokes
        speak("My developer did not teach me how to tell jokes ... Ha ha ha")

    else:
        print('I didn\'t get you, can you repeat?')


# Launch
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[1].id)

# forced cmd test
speak("Let\'s get ready!")

speak("Hi, I'm Sia")
speak("I am listening to you")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop