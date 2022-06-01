"""rooms

Revision ID: 8fee61d83268
Revises: 0010bc73c52e
Create Date: 2021-12-13 14:37:28.381738

"""
from typing import Tuple

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8fee61d83268'
down_revision = '0010bc73c52e'
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def upgrade():
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    op.create_table('rooms',
                    sa.Column("id", sa.Integer),
                    sa.Column("name", sa.String(255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    *timestamps(),
                    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)

    op.create_table('messages',
                    sa.Column("id", sa.Integer),
                    sa.Column("room_id", sa.Integer, nullable=False),
                    sa.Column("user_id", sa.Integer, nullable=False),
                    sa.Column("content", sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
                    sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ),
                    sa.PrimaryKeyConstraint('id'),
                    *timestamps(),
                    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')

    op.create_table('messages',
                    sa.Column("id", sa.Integer),
                    sa.Column("user_id", sa.Integer, nullable=False),
                    sa.Column("content", sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
                    sa.PrimaryKeyConstraint('id'),
                    *timestamps(),
                    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)