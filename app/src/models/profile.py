from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_setup import Base  # <--- Stessa Base comune

# Questo blocco viene letto solo dai linter/IDE, non all'esecuzione
if TYPE_CHECKING:
	from models.user import User


class Profile(Base):
	__tablename__ = 'profiles'

	id: Mapped[int] = mapped_column(primary_key=True)
	bio: Mapped[str | None] = mapped_column()
	avatar_url: Mapped[str | None] = mapped_column(String(255))

	# Chiave esterna che collega il profilo all'utente
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)

	# Relazione speculare verso l'utente
	user: Mapped['User'] = relationship('User', back_populates='profile')
