"""Modifica la tabella employee

Revision ID: d88e0ca93edf
Revises:
Create Date: 2026-06-06 11:11:01.541485

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd88e0ca93edf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	"""Upgrade schema."""
	op.create_table(
		'employees',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('name', sa.String(50), nullable=False),
		sa.Column('last_name', sa.String(50), nullable=True),
	)


def downgrade() -> None:
	"""Downgrade schema."""
	op.drop_table('employees')
