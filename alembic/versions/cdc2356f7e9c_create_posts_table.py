"""create Posts table

Revision ID: cdc2356f7e9c
Revises: 
Create Date: 2023-06-30 15:04:14.139762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdc2356f7e9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
