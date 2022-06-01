"""message_threats

Revision ID: a2cde970dd16
Revises: 7a1bd08e6c4f
Create Date: 2022-01-24 09:41:27.066395

"""
from typing import Tuple

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2cde970dd16'
down_revision = '7a1bd08e6c4f'
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
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
    op.create_table('message_threads',
                    sa.Column("id", sa.Integer),
                    sa.Column("message_id", sa.Integer, nullable=False),
                    sa.Column("user_id", sa.Integer, nullable=False),
                    sa.Column("content", sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(["message_id"], ["messages.id"], ),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
                    sa.PrimaryKeyConstraint('id'),
                    *timestamps(),
                    )
    op.create_index(op.f('ix_message_threads_id'), 'message_threads', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_message_threads_id'), table_name='message_threads')
    op.drop_table('message_threads')
