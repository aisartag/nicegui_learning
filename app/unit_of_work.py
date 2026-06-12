import logging
from types import TracebackType
from typing import Type

from core.log_loader import configExtra
from database.engine import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


class UnitOfWork:
	def __init__(self, session_factory: async_sessionmaker[AsyncSession] = AsyncSessionLocal):
		self.session_factory = session_factory
		# Usiamo un attributo privato per il tracking interno
		self._session: AsyncSession | None = None

	async def __aenter__(self):
		self._session = self.session_factory()
		await self._session.begin()
		return self

	async def __aexit__(
		self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
	):
		if self._session:
			try:
				if exc_type is None:
					await self._session.commit()
				else:
					await self._session.rollback()
			finally:
				await self._session.close()
				self._session = None

	# Questa property risolve i problemi di Pylance!
	@property
	def session(self) -> AsyncSession:
		if self._session is None:
			raise RuntimeError("L'Unit of Work non è attivo. Usa il blocco 'async with'.")
		return self._session
