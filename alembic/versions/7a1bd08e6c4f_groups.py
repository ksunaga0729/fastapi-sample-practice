"""member

Revision ID: 7a1bd08e6c4f
Revises: 8fee61d83268
Create Date: 2021-12-20 13:34:52.971083

"""
from alembic import op
import sqlalchemy as sa

from typing import Tuple

# revision identifiers, used by Alembic.
revision = '7a1bd08e6c4f'
down_revision = '8fee61d83268'
branch_labels = None
depends_on = None


def timestamps(indexed: bool = False) -> Tuple[sa.Column]:
    return (
        sa.Column(
            "read_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def upgrade():
    op.create_table('room_members',
                    sa.Column("user_id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("room_id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("member_role", sa.String(255), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ),
                    sa.ForeignKeyConstraint(["room_id"], ["rooms.id"],),
                    *timestamps(),
                    )


def downgrade():
    op.drop_table('room_members')
