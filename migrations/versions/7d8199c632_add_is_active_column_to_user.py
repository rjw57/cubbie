"""add is_active column to user

Revision ID: 7d8199c632
Revises: 11680e8c4bf
Create Date: 2015-03-12 13:03:37.654960

"""

# revision identifiers, used by Alembic.
revision = '7d8199c632'
down_revision = '11680e8c4bf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add is_active column to users initially marking all users as active
    op.add_column('users', sa.Column('is_active', sa.Boolean(),
        server_default=sa.text("'1'"), nullable=False))

    # Now alter the column s.t. new users are *inactive*.
    op.alter_column('users', 'is_active', server_default=sa.text("'0'"))

def downgrade():
    op.drop_column('users', 'is_active')
