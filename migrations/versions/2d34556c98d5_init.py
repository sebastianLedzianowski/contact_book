"""Init

Revision ID: 2d34556c98d5
Revises: d5e6d9b44ceb
Create Date: 2024-01-31 19:24:54.435873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d34556c98d5'
down_revision: Union[str, None] = 'd5e6d9b44ceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'phone_number',
               existing_type=sa.VARCHAR(length=15),
               type_=sa.String(length=30),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'phone_number',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=15),
               existing_nullable=True)
    # ### end Alembic commands ###
