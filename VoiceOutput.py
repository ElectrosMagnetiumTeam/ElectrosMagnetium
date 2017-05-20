from subprocess import Popen, PIPE

class VoiceOutput(object):
    def __init__(self):
        """
        Initialize the voice output module
        """
        print '[VoiceOutput] instance initiallized'

    def say(self, phrase):
        """
        Say the given phrase.
        """
        print '[VoiceOutput] saying phrase: {}'.format(phrase)
        proc = Popen(['festival', '--tts'], stdin=PIPE)
        proc.stdin.write(phrase)
        proc.stdin.close()
        proc.wait()
