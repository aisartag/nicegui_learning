# from typing import cast

# from auth.services.user_state import UserState
# from models.user import User
# from nicegui import app


# def logout() -> None:
# 	"""
# 	Sconnette l'utente cancellando la sessione dallo storage di NiceGUI.
# 	Questo metodo può essere sincrono perché agisce solo sullo storage locale.
# 	"""
# 	# Cancelliamo le chiavi di autenticazione
# 	app.storage.user.pop('authenticated', None)
# 	app.storage.user.pop('user_id', None)
# 	app.storage.user.pop('username', None)

# 	# In alternativa, per svuotare completamente tutto lo storage dell'utente:
# 	# app.storage.user.clear()


# def get_authenticate_username() -> str:
# 	return cast(dict[str, str], app.storage.user).get('username', 'U')


# def get_authenticated_user_id() -> int | None:
# 	return cast(dict[str, int], app.storage.user).get('user_id', None)


# def storage_current_user_state(user_orm: User):
# 	app.storage.client['user_state'] = UserState.from_orm(user_orm)


# def get_current_user_state() -> UserState | None:
# 	return cast(dict[str, UserState], app.storage.client).get('user_state', None)
