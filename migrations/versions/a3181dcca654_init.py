"""Init

Revision ID: a3181dcca654
Revises: 165163ec3e6a
Create Date: 2024-01-31 14:26:02.124795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3181dcca654'
down_revision: Union[str, None] = '165163ec3e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('lastname', sa.String(length=50), nullable=False))
    op.add_column('contact', sa.Column('done', sa.Boolean(), nullable=True))
    op.drop_column('contact', 'surname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('surname', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_column('contact', 'done')
    op.drop_column('contact', 'lastname')
    # ### end Alembic commands ###
