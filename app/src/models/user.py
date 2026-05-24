from __future__ import annotations

from typing import TYPE_CHECKING

from database.engine import Base  # <--- Importiamo la Base comune
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Questo blocco viene letto solo dai linter/IDE, non all'esecuzione
if TYPE_CHECKING:
	from models.profile import Profile


class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	password: Mapped[str] = mapped_column(String(255), nullable=False)

	# Relazione verso il profilo (Uno-a-Uno)
	# back_populates indica il nome dell'attributo speculare nella classe Profile
	profile: Mapped['Profile'] = relationship('Profile', back_populates='user', uselist=False)
