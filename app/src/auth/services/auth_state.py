import logging
from typing import cast

from core.log_loader import configExtra
from nicegui import app

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class AuthState:
	@classmethod
	def is_authenticated(cls) -> bool:
		return cast(dict[str, bool], app.storage.user).get('authenticated', False)

	@classmethod
	def get_authenticate_username(cls) -> str:
		return cast(dict[str, str], app.storage.user).get('username', 'U')

	@classmethod
	def get_authenticated_user_id(cls) -> int | None:
		if not cls.is_authenticated():
			return None
		return cast(dict[str, int], app.storage.user).get('user_id', None)

	@classmethod
	def logout(cls) -> None:
		"""
		Sconnette l'utente cancellando la sessione dallo storage di NiceGUI.
		Questo metodo può essere sincrono perché agisce solo sullo storage locale.
		"""
		# Cancelliamo le chiavi di autenticazione
		app.storage.user.pop('authenticated', None)
		app.storage.user.pop('user_id', None)
		app.storage.user.pop('username', None)

		app.storage.client.pop('user_state', None)

		# In alternativa, per svuotare completamente tutto lo storage dell'utente:
		# app.storage.user.clear()
		# negata per presenza dati tema
