"""adicionando campo isActive em flock

Revision ID: fbfe652544ba
Revises: c615020ec165
Create Date: 2025-06-29 05:03:48.825614

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fbfe652544ba"
down_revision: Union[str, Sequence[str], None] = "c615020ec165"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("flock", sa.Column("isActive", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("flock", "isActive")
    # ### end Alembic commands ###
