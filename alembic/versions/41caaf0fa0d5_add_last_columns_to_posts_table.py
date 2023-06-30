"""add last columns to posts table

Revision ID: 41caaf0fa0d5
Revises: 6f730be77d69
Create Date: 2023-06-30 16:12:27.377586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41caaf0fa0d5'
down_revision = '6f730be77d69'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at',
                                     sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column(table_name='posts', column_name='published')
    op.drop_column(table_name='posts', column_name='created_at')
    pass
