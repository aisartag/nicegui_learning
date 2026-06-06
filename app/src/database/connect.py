import models
from database.engine import engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError


async def do_connection(reset: bool = False) -> bool:

	try:
		async with engine.begin() as conn:
			if reset:
				await conn.run_sync(models.Base.metadata.drop_all)  # solo in sviluppo

			await conn.run_sync(models.Base.metadata.create_all)
			return True

	except OperationalError as e:
		print(f'Errore di rete o di autenticazione (DB Offline o credenziali errate): {e}')
		return False
	except SQLAlchemyError as e:
		print(f'Si è verificato un errore generico in SQLAlchemy: {e}')
		return False
	except Exception as e:
		print(f'Si è verificato un errore generico: {e}')
		return False
	finally:
		print('Dispose engine db')
		await engine.dispose()
