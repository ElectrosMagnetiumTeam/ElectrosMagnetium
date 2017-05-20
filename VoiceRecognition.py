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

    def recognize(self, keywords):
        """
        Recognize the spoken word from a keywords list (e.g. ["one", "two", "three"]).
        returns the found keyword or None.
        """
        print '[VoiceRecognition] Say something from the following list: {}!'.format(keywords)

        with self._microphone: 
            audio = self._recognizer.listen(self._microphone)

        print '[VoiceRecognition] Got it! Now to recognize it...'
        try:
            # recognize speech using Sphinx
            value = self._recognizer.recognize_sphinx(audio, keyword_entries=keywords)
            print u'[VoiceRecognition] You said {}'.format(value).encode("utf-8")

        except speech_recognition.UnknownValueError:
            print '[VoiceRecognition] Oops! Didn\'t catch that'
        except speech_recognition.RequestError as e:
            print '[VoiceRecognition] Uh oh! Couldn\'t request results from the speach recognition source; {0}'.format(e)

        # we have to return a keyword
        return value
