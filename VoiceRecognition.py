class VoiceRecognition(object):
	def __init__(self):
		"""
		Initialize the voice recognition module
		"""
		print '[VoiceRecognition] instance initiallized'

	def recognize(self, keywords):
		"""
		Recognize the spoken word from a keywords list (e.g. ["one", "two", "three"]).
		returns the found keyword or None.
		"""
		print '[VoiceRecognition] trying to recognize a word from the following list: {}'.format(keywords)
