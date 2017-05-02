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
