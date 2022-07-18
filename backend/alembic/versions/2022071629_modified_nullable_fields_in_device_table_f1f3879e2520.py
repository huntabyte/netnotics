"""modified nullable fields in device table

Revision ID: f1f3879e2520
Revises: 193209bac4e9
Create Date: 2022-07-16 21:29:17.740567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1f3879e2520"
down_revision = "193209bac4e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "devices", "ip_address", existing_type=sa.VARCHAR(length=128), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "devices", "ip_address", existing_type=sa.VARCHAR(length=128), nullable=False
    )
    # ### end Alembic commands ###