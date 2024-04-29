"""create plan table

Revision ID: 899c5c173212
Revises: 26154e35f873
Create Date: 2024-04-29 10:49:07.522536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '899c5c173212'
down_revision: Union[str, None] = '26154e35f873'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "plans",
        sa.Column("id", sa.UUID, primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("modified_at", sa.DateTime),

        sa.Column("name", sa.String(5), unique=True, nullable=False),
        sa.Column("instance_id", sa.UUID, sa.ForeignKey(
            "instances.id"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("plans")
