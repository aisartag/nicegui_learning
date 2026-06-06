class RegistrationException(Exception):
	"""Sollevata quando l'email o username è già registrata nel sistema."""

	def __init__(self, message: str = 'Errore di integrià nei dati.'):
		self.message = message
		super().__init__(self.message)


class InvalidCredentialsException(Exception):
	"""Eccezione sollevata quando l'email o la password sono errate."""

	def __init__(self, message: str = 'Email o password non valide'):
		self.message = message
		super().__init__(self.message)


class UnAuthenticatedException(Exception):
	"""Eccezione sollevata quando viene richiesto user_state ma non esiste."""

	def __init__(self, message: str = 'Utente non autenticato'):
		self.message = message
		super().__init__(self.message)
