"""initial schema

Revision ID: e64cd1af67
Revises: None
Create Date: 2015-03-10 00:40:22.797213

"""

# revision identifiers, used by Alembic.
revision = 'e64cd1af67'
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
    op.create_table('productions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_production_name', 'productions', ['name'], unique=False)
    op.create_index('idx_production_slug', 'productions', ['slug'], unique=False)
    op.create_table('performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('starts_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('ends_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('production_id', sa.Integer(), nullable=False),
    sa.Column('is_cancelled', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.CheckConstraint('ends_at > starts_at'),
    sa.ForeignKeyConstraint(['production_id'], ['productions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_performance_is_cancelled', 'performances', ['is_cancelled'], unique=False)
    op.create_index('idx_performance_is_deleted', 'performances', ['is_deleted'], unique=False)
    op.create_index('idx_performance_production', 'performances', ['production_id'], unique=False)
    op.create_index('idx_performance_starts_at', 'performances', ['starts_at'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measured_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('performance_id', sa.Integer(), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=False),
    sa.Column('available', sa.Integer(), nullable=False),
    sa.CheckConstraint('sold <= available'),
    sa.CheckConstraint('sold >= 0'),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sales_is_valid', 'sales', ['is_valid'], unique=False)
    op.create_index('idx_sales_measured_at', 'sales', ['measured_at'], unique=False)
    op.create_index('idx_sales_performance', 'sales', ['performance_id'], unique=False)


def downgrade():
    op.drop_index('idx_sales_performance', table_name='sales')
    op.drop_index('idx_sales_measured_at', table_name='sales')
    op.drop_index('idx_sales_is_valid', table_name='sales')
    op.drop_table('sales')
    op.drop_index('idx_performance_starts_at', table_name='performances')
    op.drop_index('idx_performance_production', table_name='performances')
    op.drop_index('idx_performance_is_deleted', table_name='performances')
    op.drop_index('idx_performance_is_cancelled', table_name='performances')
    op.drop_table('performances')
    op.drop_index('idx_production_slug', table_name='productions')
    op.drop_index('idx_production_name', table_name='productions')
    op.drop_table('productions')
    op.drop_index('idx_user_displayname', table_name='users')
    op.drop_table('users')
