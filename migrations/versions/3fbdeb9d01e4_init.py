"""Init

Revision ID: 3fbdeb9d01e4
Revises: a3181dcca654
Create Date: 2024-01-31 14:46:04.911666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fbdeb9d01e4'
down_revision: Union[str, None] = 'a3181dcca654'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'email')
    op.drop_column('contact', 'phone_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('phone_number', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    op.add_column('contact', sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
