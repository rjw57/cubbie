"""create user table

Revision ID: 2087b9cbc1e
Revises: None
Create Date: 2015-03-09 19:22:03.312067

"""

# revision identifiers, used by Alembic.
revision = '2087b9cbc1e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('displayname', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_user_displayname', 'users', ['displayname'])

def downgrade():
    op.drop_table('users')
