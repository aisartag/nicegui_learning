import os
import sys

# postgresql+asyncpg://user:password@db:5432/nicegui_db
# Legge l'URL dal Docker Compose
from dotenv import load_dotenv
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()
DB_URL = os.environ.get('DB_URL', 'pippe')

print(DB_URL)

try:
	# Motore asincrono
	engine = create_async_engine(DB_URL, echo=True)

	# Generatore di sessioni
	AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

except ArgumentError as e:
	# Catturiamo l'errore della stringa malformata
	print('\n' + '=' * 60)
	print('ERRORE CRITICO CONFIGURAZIONE DATABASE:')
	print('La stringa DB_URL fornita non è un URL valido per SQLAlchemy.')
	print(f'Dettaglio: {e}')
	print("Verifica il file .env o le variabili d'ambiente di Docker Compose.")
	print('=' * 60 + '\n')

	# Invece di fare 'raise', usiamo sys.exit(1) per spegnere l'applicazione
	# senza sputare fuori tutto lo stack trace nel terminale.
	sys.exit(1)


class Base(DeclarativeBase):
	pass
