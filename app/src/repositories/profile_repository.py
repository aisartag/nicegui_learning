# repositories/profile_repository.py
from models.profile import Profile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ProfileRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_for_user(self, user_id: int, bio: str | None = None) -> Profile:
		"""Crea il profilo agganciandolo all'ID utente generato dal flush."""
		new_profile = Profile(user_id=user_id, bio=bio)
		self.session.add(new_profile)

		# Non serve il commit qui, lo farà il Service alla fine del blocco 'async with session.begin()'
		await self.session.flush()
		return new_profile

	async def update_avatar_path(self, user_id: int, avatar_path: str):
		profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

		if not profile:
			raise ValueError(f"Profilo non trovato per l'utente {user_id}")

		profile.avatar_url = avatar_path

		return profile

	async def update_bio(self, user_id: int, bio: str | None):
		profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

		if not profile:
			raise ValueError(f"Profilo non trovato per l'utente {user_id}")

		profile.bio = bio

		return profile
