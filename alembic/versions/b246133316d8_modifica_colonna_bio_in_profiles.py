"""Modifica colonna bio in profiles

Revision ID: b246133316d8
Revises: d88e0ca93edf
Create Date: 2026-06-06 15:06:49.789256

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b246133316d8'
down_revision: Union[str, Sequence[str], None] = 'd88e0ca93edf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	"""Upgrade schema."""
	op.alter_column('profiles', 'bio', type_=sa.String())


def downgrade() -> None:
	"""Downgrade schema."""
	op.alter_column('profiles', 'bio', type_=sa.String(500))
