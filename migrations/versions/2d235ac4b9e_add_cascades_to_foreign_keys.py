"""add cascades to foreign keys

Revision ID: 2d235ac4b9e
Revises: 7d8199c632
Create Date: 2015-03-20 10:11:40.618169

"""

# revision identifiers, used by Alembic.
revision = '2d235ac4b9e'
down_revision = '7d8199c632'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('user_identities_user_id_fkey', 'user_identities')
    op.create_foreign_key(
        'user_identities_user_id_fkey', 'user_identities', 'users',
        ['user_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('capabilities_user_id_fkey', 'capabilities')
    op.create_foreign_key(
        'capabilities_user_id_fkey', 'capabilities', 'users',
        ['user_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('sales_performance_id_fkey', 'sales')
    op.create_foreign_key(
        'sales_performance_id_fkey', 'sales', 'performances',
        ['performance_id'], ['id'], ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('user_identities_user_id_fkey', 'user_identities')
    op.create_foreign_key(
        'user_identities_user_id_fkey', 'user_identities', 'users',
        ['user_id'], ['id']
    )

    op.drop_constraint('capabilities_user_id_fkey', 'capabilities')
    op.create_foreign_key(
        'capabilities_user_id_fkey', 'capabilities', 'users',
        ['user_id'], ['id']
    )

    op.drop_constraint('sales_performance_id_fkey', 'sales')
    op.create_foreign_key(
        'sales_performance_id_fkey', 'sales', 'performances',
        ['performance_id'], ['id']
    )
