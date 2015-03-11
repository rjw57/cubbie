"""add random_id for users, productions and performances

Revision ID: 11680e8c4bf
Revises: 48567f3faf
Create Date: 2015-03-11 20:29:18.326587

"""

# revision identifiers, used by Alembic.
revision = '11680e8c4bf'
down_revision = '48567f3faf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('CREATE SEQUENCE random_id_seq')
    op.execute('''
-- Return an id which is a hybrid of sequential and
-- random values.
CREATE OR REPLACE FUNCTION random_id() RETURNS bigint AS $$
DECLARE
    epoch bigint := 13149;
    rnd_portion bigint;
    seq_portion bigint;
BEGIN
    seq_portion := epoch + nextval('random_id_seq');
    rnd_portion := trunc((random() * 9999) + 1);
    return (seq_portion * 10000) + rnd_portion;
END
$$ LANGUAGE plpgsql;
''')
    op.alter_column('users', 'id', server_default=sa.text('random_id()'))
    op.alter_column('productions', 'id', server_default=sa.text('random_id()'))
    op.alter_column('performances', 'id', server_default=sa.text('random_id()'))

def downgrade():
    op.alter_column('users', 'id', server_default=None)
    op.alter_column('productions', 'id', server_default=None)
    op.alter_column('performances', 'id', server_default=None)
    op.execute('DROP FUNCTION random_id()')
    op.execute('DROP SEQUENCE random_id_seq')
