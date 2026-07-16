from typing import Any, Optional, cast

from nicegui import app
from pydantic import BaseModel, ConfigDict

from src.exceptions import UnAuthenticatedException
from src.models.user import User


class ProfileState(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	bio: Optional[str] = None
	avatar_url: Optional[str] = None


class UserState(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	username: str
	email: str
	profile: Optional[ProfileState] = None


class UserStateService:
	@staticmethod
	def on_login(user_orm: User):

		# Popoliamo la struttura Pydantic tramite model_validate
		user_state = UserState.model_validate(user_orm)

		# SETTIAMO IL PAYLOAD MINIMO E LEGGERO NEL COOKIE
		app.storage.user['authenticated'] = True
		app.storage.user['user_id'] = user_state.id
		app.storage.user['username'] = user_state.username

		# Se vuoi salvare TUTTO lo UserState in modo persistente e sicuro per l'utente,
		# senza toccare variabili globali, lo serializzi in un dizionario dentro lo storage user:
		app.storage.user['cached_state'] = user_state.model_dump()

	@staticmethod
	def is_authenticated() -> bool:
		return cast(dict[str, Any], app.storage.user).get('authenticated', False)

	@staticmethod
	def get_user_id() -> int | None:
		return cast(dict[str, Any], app.storage.user).get('user_id', None)

	@staticmethod
	def on_logout():
		app.storage.user.clear()

	@staticmethod
	def get_cached_state() -> UserState | None:
		if not cast(dict[str, Any], app.storage.user).get('authenticated', False):
			return None

		state_dict = cast(dict[str, Any], app.storage.user).get('cached_state', None)

		if state_dict is None:
			return None

		return UserState.model_validate(state_dict) or None

	@staticmethod
	def update_user_profile_avatar_url(url: str):
		user_state = UserStateService.get_cached_state()
		if user_state is None or user_state.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		updated_profile = user_state.profile.model_copy(update={'avatar_url': url})
		updated_user = user_state.model_copy(update={'profile': updated_profile})
		app.storage.user['cached_state'] = updated_user.model_dump()

	@staticmethod
	def update_user_profile_bio(bio: str | None):
		user_state = UserStateService.get_cached_state()
		if user_state is None or user_state.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		updated_profile = user_state.profile.model_copy(update={'bio': bio})
		updated_user = user_state.model_copy(update={'profile': updated_profile})
		app.storage.user['cached_state'] = updated_user.model_dump()
