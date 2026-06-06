from dataclasses import dataclass

from models.user import User


@dataclass
class ProfileState:
	id: int
	bio: str | None = None
	avatar: str | None = None


@dataclass
class UserState:
	id: int
	username: str
	email: str
	profile: ProfileState | None = None

	@classmethod
	def from_orm(cls, user_orm: User) -> 'UserState':
		"""Metodo di utilità per convertire l'oggetto SQLAlchemy (ORM)
		direttamente in questo oggetto di stato per la UI.
		"""
		profile_state = None
		if user_orm.profile:
			profile_state = ProfileState(
				id=user_orm.profile.id, bio=user_orm.profile.bio, avatar=user_orm.profile.avatar_url
			)

		return cls(id=user_orm.id, username=user_orm.username, email=user_orm.email, profile=profile_state)
