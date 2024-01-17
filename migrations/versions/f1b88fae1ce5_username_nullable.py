"""Username nullable

Revision ID: f1b88fae1ce5
Revises: 6474d6157542
Create Date: 2023-11-22 22:50:31.206638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1b88fae1ce5'
down_revision: Union[str, None] = '6474d6157542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
