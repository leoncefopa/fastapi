"""add content column to posts table

Revision ID: bffec3eda004
Revises: cdc2356f7e9c
Create Date: 2023-06-30 15:13:59.467318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bffec3eda004'
down_revision = 'cdc2356f7e9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
