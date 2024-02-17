"""Init

Revision ID: d5e6d9b44ceb
Revises: 77652c0b7ff5
Create Date: 2024-01-31 15:21:06.695948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e6d9b44ceb'
down_revision: Union[str, None] = '77652c0b7ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('email', sa.String(length=50), nullable=True))
    op.add_column('contact', sa.Column('phone_number', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'phone_number')
    op.drop_column('contact', 'email')
    # ### end Alembic commands ###
