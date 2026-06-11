import asyncio
import hashlib
import logging
from pathlib import Path

from core.log_loader import configExtra
from core.paths import ProjectPaths
from exceptions import RegistrationException
from models.user import User
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository
from services.crypto_service import CryptoService  # Nuovo import
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UserService:
	def __init__(self, session: AsyncSession):
		self.session = session
		self.user_repo = UserRepository(self.session)
		self.profile_repo = ProfileRepository(self.session)

	async def register_user_with_profile(
		self, username: str, email: str, clear_password: str, bio: str | None = None
	) -> User:
		"""
		Registra un nuovo utente cifrando la password e creando il profilo in modo atomico.
		"""

		logger.info(f'Registrazione di un nuovo utente: {username} {email} {clear_password}')

		# 1. Il try avvolge TUTTA la transazione, incluso il commit automatico di begin()
		try:
			async with self.session.begin():
				# Controlli preventivi (facoltativi ma utili per messaggi puliti)
				existing_email = await self.user_repo.get_user_by_email(email)
				if existing_email:
					raise ValueError(f"L'email '{email}' è già associata a un account.")

				existing_name = await self.user_repo.get_user_by_name(username)
				if existing_name:
					raise ValueError(f"Lo username '{username}' è già in uso.")

				# Logica di business
				password_hash = CryptoService.hash_password(clear_password)
				user_orm = await self.user_repo.create(username=username, email=email, password_hash=password_hash)

				# Invia i dati a Postgres per generare l'ID (scatta IntegrityError se c'è un duplicato concorrente)
				await self.session.flush()

				# Creazione del profilo legato
				await self.profile_repo.create_for_user(user_id=user_orm.id, bio=bio)

				# Qui finisce il blocco: SQLAlchemy prova a fare il COMMIT.
				# Se il commit fallisce, salta direttamente all'except esterno.

			# Se siamo qui, il commit è riuscito al 100%
			return user_orm

		# 2. Gestisci separatamente i tuoi errori di validazione da quelli del DB
		except ValueError as val_error:
			# Rilancia l'errore di validazione così com'è per NiceGUI (es. "Email già in uso")
			raise val_error

		except IntegrityError as db_error:  # pyright: ignore[reportUnusedVariable] # noqa: F841
			# Se il vincolo UNIQUE del DB salta (es. registrazione simultanea)
			raise RegistrationException('Errore di integrità dei dati durante la registrazione.')

		except Exception as generic_error:
			# Qualsiasi altro errore imprevisto (connessione persa, crash, ecc.)
			raise RegistrationException(f'Errore imprevisto durante la registrazione: {generic_error}')

	async def get_user_with_profile(self, user_id: int) -> User | None:
		"""Cerca un utente tramite ID (Asincrono)."""
		user = await self.user_repo.get_user_with_profile(user_id)

		return user

	async def save_avatar(self, user_id: int, original_filename: str, file_bytes: bytes) -> str:
		"""
		Salva l'avatar di un utente.

		Args:
			user_id (int): L'ID dell'utente.
			original_filename (str): Il nome originale del file.
			file_bytes (bytes): I byte del file.

		Returns:
			str: Il percorso relativo dell'avatar salvato.
		"""
		logger.info(f'Salvataggio avatar per utente {user_id}...')

		user_hash = hashlib.md5(str(user_id).encode('utf-8')).hexdigest()

		ext = Path(original_filename).suffix.lower()
		nome_file = f'{user_hash}{ext}'

		target_folder = ProjectPaths.DATA_STORAGE_AVATARS / user_hash[0:2] / user_hash[2:4]
		target_folder.mkdir(parents=True, exist_ok=True)

		for file_exists in target_folder.glob(f'{user_hash}.*'):
			try:
				if file_exists.is_file():
					file_exists.unlink()  # Versione moderna di os.remove con pathlib
			except Exception as ex:
				raise Exception(f"Errore durante l'eliminazione del vecchio avatar: {ex}")

		full_path_file = target_folder / nome_file
		# with open(full_path_file, 'wb') as f:
		# 	f.write(file_bytes)

		db_relative_path = f'uploads/{user_hash[0:2]}/{user_hash[2:4]}/{nome_file}'
		# 1. Scrittura del NUOVO file in modo ASINCRONO per non bloccare NiceGUI
		try:
			# Esegue la scrittura sincrona in un thread thread-pool separato
			await asyncio.to_thread(self._write_file_sync, full_path_file, file_bytes)
		except Exception as ex:
			raise IOError(f'Impossibile scrivere il file sul disco: {ex}')

		# 6. Azione del Repository con Protezione (Try/Except)
		try:
			async with self.session.begin():
				await self.profile_repo.update_avatar_path(user_id, db_relative_path)
			return db_relative_path

		except Exception as db_error:
			# # SE IL REPOSITORY FALLISCE: roll-back del file fisico
			def _rollback_disk_sync():
				if full_path_file.exists():
					full_path_file.unlink()

			await asyncio.to_thread(_rollback_disk_sync)
			logger.error(f'Salvataggio DB fallito per utente {user_id}. File di rollback rimosso.')
			raise Exception(f'Salvataggio Database fallito, rollback file eseguito: {db_error}')

	async def save_bio(self, user_id: int, bio: str | None):
		try:
			async with self.session.begin():
				return await self.profile_repo.update_bio(user_id, bio)
		except Exception as db_error:
			raise Exception(f'Salvataggio Database fallito, rollback file eseguito: {db_error}')

	def _write_file_sync(self, path: Path, data: bytes):
		"""Funzione helper sincrona da eseguire nel thread pool."""
		with open(path, 'wb') as f:
			f.write(data)
