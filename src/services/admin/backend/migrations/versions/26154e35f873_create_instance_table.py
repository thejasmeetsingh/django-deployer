"""create instance table

Revision ID: 26154e35f873
Revises: 
Create Date: 2024-04-29 15:30:58.966436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26154e35f873'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "instances",
        sa.Column("id", sa.UUID, primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("modified_at", sa.DateTime),

        sa.Column("type", sa.String(50), nullable=False, unique=True)
    )


def downgrade() -> None:
    op.drop_table("instances")
