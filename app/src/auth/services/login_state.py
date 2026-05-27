from typing import cast

from nicegui import app


def logout() -> None:
	"""
	Sconnette l'utente cancellando la sessione dallo storage di NiceGUI.
	Questo metodo può essere sincrono perché agisce solo sullo storage locale.
	"""
	# Cancelliamo le chiavi di autenticazione
	app.storage.user.pop('authenticated', None)
	app.storage.user.pop('user_id', None)
	app.storage.user.pop('username', None)

	# In alternativa, per svuotare completamente tutto lo storage dell'utente:
	# app.storage.user.clear()


def is_loggedin() -> bool:
	return cast(dict[str, bool], app.storage.user).get('authenticated', False)


def get_logged_username() -> str:
	return cast(dict[str, str], app.storage.user).get('username', 'U')
