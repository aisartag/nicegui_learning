# services/auth_service.py


from exceptions import InvalidCredentialsException
from models.user import User

# from nicegui import app
from repositories.user_repository import UserRepository
from services.crypto_service import CryptoService
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
	def __init__(self, session: AsyncSession):
		self.session = session
		self.user_repo = UserRepository(self.session)

	async def verify_credential(self, email: str, clear_password: str) -> User | None:
		"""
		Verifica le credenziali e avvia la sessione in NiceGUI.
		Ritorna True se il login ha successo, False altrimenti.
		"""

		user_orm = await self.user_repo.get_user_with_profile_by_email(email)

		if not user_orm:
			return None  # Utente non trovato

		# 2. Verifichiamo se la password corrisponde all'hash salvato
		is_valid = CryptoService.verify_password(clear_password, user_orm.password)
		if not is_valid:
			return None  # Password errata

		if not user_orm or not CryptoService.verify_password(clear_password, user_orm.password):
			raise InvalidCredentialsException()

		return user_orm
