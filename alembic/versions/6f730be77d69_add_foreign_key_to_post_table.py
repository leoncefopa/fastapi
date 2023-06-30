"""add foreign key to post table

Revision ID: 6f730be77d69
Revises: 594e9ebce5f3
Create Date: 2023-06-30 16:02:26.393678

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6f730be77d69'
down_revision = '594e9ebce5f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['user_id'], ondelete='CASCADE'
                          )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
