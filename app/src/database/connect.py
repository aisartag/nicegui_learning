import logging

from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.core.setting_setup import SettingInit
from src.database.db_setup import Base, engine

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


async def db_init(reset: bool = False) -> bool:

	try:
		async with engine.begin() as conn:
			if reset:
				await conn.run_sync(Base.metadata.drop_all)  # solo in sviluppo se necessario

			await conn.run_sync(Base.metadata.create_all)
			return True

	except OperationalError as e:
		logger.error(f'Errore di rete o di autenticazione (DB Offline o credenziali errate): {e}')
		return False
	except SQLAlchemyError as e:
		logger.error(f'Si è verificato un errore generico in SQLAlchemy: {e}')
		return False
	except Exception as e:
		logger.error(f'Si è verificato un errore generico: {e}')
		return False
	finally:
		await engine.dispose()
