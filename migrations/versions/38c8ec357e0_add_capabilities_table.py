"""add capabilities table

Revision ID: 38c8ec357e0
Revises: e64cd1af67
Create Date: 2015-03-10 13:24:16.971933

"""

# revision identifiers, used by Alembic.
revision = '38c8ec357e0'
down_revision = 'e64cd1af67'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('capabilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('production_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('member', 'operator', 'admin', name='capability'), nullable=False),
    sa.ForeignKeyConstraint(['production_id'], ['productions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_capabilities_production', 'capabilities', ['production_id'], unique=False)
    op.create_index('idx_capabilities_user', 'capabilities', ['user_id'], unique=False)


def downgrade():
    op.drop_index('idx_capabilities_user', table_name='capabilities')
    op.drop_index('idx_capabilities_production', table_name='capabilities')
    op.drop_table('capabilities')

    # Enum type created for type column
    op.execute('DROP TYPE capability')
