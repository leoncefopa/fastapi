"""add user table

Revision ID: 594e9ebce5f3
Revises: bffec3eda004
Create Date: 2023-06-30 15:33:52.091073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '594e9ebce5f3'
down_revision = 'bffec3eda004'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
