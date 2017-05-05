#!/usr/bin/env python
#
# In order to run, you have to install the following:
# sudo apt-get install python python-dev python-pip build-essential swig git libpulse-dev python-pyaudio python3-pyaudio
# sudo -H pip install --upgrade pip setuptools wheel
# sudo -H pip install pocketsphinx SpeechRecognition

import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

entries = None
# if you only want specific words, uncomment the following line (the numbers represent sensitivity):
# entries = [("one", 1.0), ("two", 1.0), ("three", 1.0)]

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Sphinx
            value = r.recognize_sphinx(audio, keyword_entries=entries)
            

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Sphinx; {0}".format(e))
except KeyboardInterrupt:
    pass

