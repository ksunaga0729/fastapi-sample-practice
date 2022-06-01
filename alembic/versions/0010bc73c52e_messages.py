"""messages

Revision ID: 0010bc73c52e
Revises: 9ee75a0ee88d
Create Date: 2021-12-01 10:31:12.603131

"""

from typing import Tuple

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0010bc73c52e'
down_revision = '9ee75a0ee88d'
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
    op.create_table('messages',
                    sa.Column("id", sa.Integer),
                    sa.Column("user_id", sa.Integer, nullable=False),
                    sa.Column("content", sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
                    sa.PrimaryKeyConstraint('id'),
                    *timestamps(),
                    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')