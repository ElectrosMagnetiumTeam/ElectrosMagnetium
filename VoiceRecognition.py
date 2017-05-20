import speech_recognition

class VoiceRecognition(object):
    def __init__(self):
        """
        Initialize the voice recognition module
        """
        self._recognizer = speech_recognition.Recognizer()
        self._microphone = speech_recognition.Microphone()
        print '[VoiceRecognition] instance initiallized'
        print '[VoiceRecognition] A moment of silence, please...'
        with self._microphone: 
            self._recognizer.adjust_for_ambient_noise(self._microphone)
        
        print '[VoiceRecognition] Set minimum energy threshold to {}'.format(self._recognizer.energy_threshold)

    def _try_recognize(self):
        """
        returns the found keyword.
        """
        value = None
        print '[VoiceRecognition] Say something!'
    
        with self._microphone: 
            audio = self._recognizer.listen(self._microphone)

        print '[VoiceRecognition] Got it! Now to recognize it...'
        try:
            # recognize speech
            value = self._recognizer.recognize_google(audio)
            print u'[VoiceRecognition] You said {}'.format(value).encode("utf-8")

        except speech_recognition.UnknownValueError:
            print '[VoiceRecognition] Oops! Didn\'t catch that'
        except speech_recognition.RequestError as e:
            print '[VoiceRecognition] Uh oh! Couldn\'t request results from the speach recognition source; {0}'.format(e)

        # we have to return a keyword
        return value

    def recognize(self):
        recognized_words = None
        while not recognized_words:
            recognized_words = self._try_recognize()

        return recognized_words
