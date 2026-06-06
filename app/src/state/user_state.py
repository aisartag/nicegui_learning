from typing import Any, Optional, cast

from exceptions import UnAuthenticatedException
from models.user import User
from nicegui import app
from pydantic import BaseModel, ConfigDict


# --- DEFINIZIONE DEI MODELLI DI STATO ---
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


# --- AL LOGIN (O AL ROOT DELL'APP) ---
# async def login_user(user_orm: User):
# 	# Genera l'oggetto di stato direttamente dall'ORM in una riga
# 	# Pydantic si occupa di mappare anche le relazioni innestate
# 	state = UserState.model_validate(user_orm)

# 	# Lo salvi direttamente come OGGETTO nello storage client
# 	app.storage.client['user_state'] = state


# def get_user_state() -> UserState | None:
# 	state_raw: Any = cast(dict[str, Any], app.storage.client).get('user_state')

# 	if state_raw is None:
# 		return None

# 	return cast(UserState, state_raw)


# def get_current_avatar_url():
# 	user_state = get_user_state()
# 	return user_state.profile.avatar_url if user_state and user_state.profile else None


# def get_current_bio():
# 	user_state = get_user_state()
# 	return user_state.profile.bio if user_state and user_state.profile else None


# def set_avatar_url(url: str):
# 	user_state = get_user_state()
# 	if user_state is None or user_state.profile is None:
# 		return
# 	user_state.profile.avatar_url = url


class UserStorage:
	# _user_state: UserState | None = None

	@classmethod
	async def login_user(cls, user_orm: User):
		# Genera l'oggetto di stato direttamente dall'ORM in una riga
		# Pydantic si occupa di mappare anche le relazioni innestate
		cls._user_state = UserState.model_validate(user_orm)

		# Lo salvi direttamente come OGGETTO nello storage client
		app.storage.client['user_state'] = cls._user_state

	@classmethod
	def get_user_state(cls) -> UserState | None:
		state_raw: Any = cast(dict[str, Any], app.storage.client).get('user_state')
		if state_raw is None:
			return None
		return cast(UserState, state_raw)

	@classmethod
	def get_profile_state(cls):
		current_user = cls.get_user_state()
		if current_user is None or current_user.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		return current_user.profile

	@classmethod
	def get_current_avatar_url(cls):
		current_user = cls.get_user_state()
		if current_user is None or current_user.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		return current_user.profile.avatar_url

	@classmethod
	def get_current_bio(cls):
		current_user = cls.get_user_state()
		if current_user is None or current_user.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		return current_user.profile.bio

	@classmethod
	def update_user_profile_avatar_url(cls, url: str):

		current_user = cls.get_user_state()
		if current_user is None or current_user.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		updated_profile = current_user.profile.model_copy(update={'avatar_url': url})
		updated_user = current_user.model_copy(update={'profile': updated_profile})
		app.storage.client['user_state'] = updated_user

	@classmethod
	def update_user_profile_bio(cls, bio: str):

		current_user = cls.get_user_state()
		if current_user is None or current_user.profile is None:
			raise UnAuthenticatedException('Utente non autenticato')

		updated_profile = current_user.profile.model_copy(update={'bio': bio})
		updated_user = current_user.model_copy(update={'profile': updated_profile})
		app.storage.client['user_state'] = updated_user
