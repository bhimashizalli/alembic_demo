"""Add priority column to tasks table

Revision ID: f8f704a101cd
Revises: c289b71f248e
Create Date: 2025-07-13 11:52:57.390173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8f704a101cd'
down_revision: Union[str, Sequence[str], None] = 'c289b71f248e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('priority', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    op.drop_column('tasks', 'priority')
    # ### end Alembic commands ###
