"""create user table

Revision ID: 4f8040bc18a
Revises: None
Create Date: 2015-03-09 21:12:59.509465

"""

# revision identifiers, used by Alembic.
revision = '4f8040bc18a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('displayname', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_displayname', 'users', ['displayname'], unique=False)


def downgrade():
    op.drop_index('idx_user_displayname', table_name='users')
    op.drop_table('users')
