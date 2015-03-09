"""create rest of initial schema

Revision ID: 3a854c963a9
Revises: 5a17d6dc829
Create Date: 2015-03-09 21:43:07.833504

"""

# revision identifiers, used by Alembic.
revision = '3a854c963a9'
down_revision = '5a17d6dc829'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('performances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('starts_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('duration', sa.Interval(), nullable=False),
    sa.Column('production_id', sa.Integer(), nullable=False),
    sa.Column('is_cancelled', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
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
    sa.Column('production_id', sa.Integer(), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=False),
    sa.Column('available', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['production_id'], ['productions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sales_is_valid', 'sales', ['is_valid'], unique=False)
    op.create_index('idx_sales_measured_at', 'sales', ['measured_at'], unique=False)
    op.create_index('idx_sales_production', 'sales', ['production_id'], unique=False)


def downgrade():
    op.drop_index('idx_sales_production', table_name='sales')
    op.drop_index('idx_sales_measured_at', table_name='sales')
    op.drop_index('idx_sales_is_valid', table_name='sales')
    op.drop_table('sales')
    op.drop_index('idx_performance_starts_at', table_name='performances')
    op.drop_index('idx_performance_production', table_name='performances')
    op.drop_index('idx_performance_is_deleted', table_name='performances')
    op.drop_index('idx_performance_is_cancelled', table_name='performances')
    op.drop_table('performances')
