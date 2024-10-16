"""update event relationship with user

Revision ID: f42de95858bf
Revises: 6cff9dbe9043
Create Date: 2024-10-13 10:24:59.257868

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f42de95858bf'
down_revision: Union[str, None] = '6cff9dbe9043'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### use batch mode for SQLite compatibility ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.Uuid(), nullable=False))
        batch_op.create_foreign_key('fk_event_owner', 'user', ['owner_id'], ['id'])


def downgrade() -> None:
    # ### use batch mode for SQLite compatibility ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('fk_event_owner', type_='foreignkey')
        batch_op.drop_column('owner_id')
