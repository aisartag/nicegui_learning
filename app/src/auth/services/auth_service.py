# services/auth_service.py


from nicegui import app
from repositories.user_repository import UserRepository
from services.crypto_service import CryptoService
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
	def __init__(self, session: AsyncSession):
		self.session = session
		self.user_repo = UserRepository(self.session)

	async def login(self, email: str, password_in_chiaro: str) -> bool:
		"""
		Verifica le credenziali e avvia la sessione in NiceGUI.
		Ritorna True se il login ha successo, False altrimenti.
		"""
		# 1. Cerchiamo l'utente nel DB tramite l'email
		user = await self.user_repo.get_by_email(email)
		if not user:
			return False  # Utente non trovato

		# 2. Verifichiamo se la password corrisponde all'hash salvato
		is_valid = CryptoService.verify_password(password_in_chiaro, user.password)
		if not is_valid:
			return False  # Password errata

		# 3. LOGIN RIUSCITO: Salviamo lo stato nello storage dell'utente di NiceGUI
		# Questi dati vengono memorizzati in un cookie cifrato lato browser
		app.storage.user['authenticated'] = True
		app.storage.user['user_id'] = user.id
		app.storage.user['username'] = user.username

		return True
