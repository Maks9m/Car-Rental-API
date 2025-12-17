"""rename book_id to booking_id

Revision ID: 7376dd384a23
Revises: a389956bf545
Create Date: 2025-12-17 11:39:31.702621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7376dd384a23'
down_revision: Union[str, Sequence[str], None] = 'a389956bf545'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('trip_book_id_fkey', 'trip', type_='foreignkey')
    op.alter_column('booking', 'book_id', new_column_name='booking_id')
    op.alter_column('trip', 'book_id', new_column_name='booking_id')
    op.drop_index('ix_booking_book_id', table_name='booking')
    op.create_index(op.f('ix_booking_booking_id'), 'booking', ['booking_id'], unique=False)
    op.drop_index('ix_trip_book_id', table_name='trip')
    op.create_index(op.f('ix_trip_booking_id'), 'trip', ['booking_id'], unique=False)
    op.create_foreign_key(None, 'trip', 'booking', ['booking_id'], ['booking_id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'trip', type_='foreignkey')
    op.alter_column('trip', 'booking_id', new_column_name='book_id')
    op.alter_column('booking', 'booking_id', new_column_name='book_id')
    op.drop_index(op.f('ix_trip_booking_id'), table_name='trip')
    op.create_index('ix_trip_book_id', 'trip', ['book_id'], unique=False)
    op.drop_index(op.f('ix_booking_booking_id'), table_name='booking')
    op.create_index('ix_booking_book_id', 'booking', ['book_id'], unique=False)
    op.create_foreign_key('trip_book_id_fkey', 'trip', 'booking', ['book_id'], ['book_id'], ondelete='SET NULL')
