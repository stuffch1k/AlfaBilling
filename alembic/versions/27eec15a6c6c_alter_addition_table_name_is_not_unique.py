"""Alter Addition table: name is not unique

Revision ID: 27eec15a6c6c
Revises: c7d523190e83
Create Date: 2024-11-07 00:20:29.287241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27eec15a6c6c'
down_revision: Union[str, None] = 'c7d523190e83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('addition_name_key', 'addition', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('addition_name_key', 'addition', ['name'])
    # ### end Alembic commands ###