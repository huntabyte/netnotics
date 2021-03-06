"""removed enums

Revision ID: 25431bb06511
Revises: 906cd977600f
Create Date: 2022-07-18 22:52:09.664212

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "25431bb06511"
down_revision = "906cd977600f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "devices",
        "vendor",
        existing_type=postgresql.ENUM("Cisco", name="vendorchoices"),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    op.alter_column(
        "devices",
        "operating_system",
        existing_type=postgresql.ENUM("IOS_XE", name="oschoices"),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "devices",
        "operating_system",
        existing_type=sa.String(length=255),
        type_=postgresql.ENUM("IOS_XE", name="oschoices"),
        existing_nullable=True,
    )
    op.alter_column(
        "devices",
        "vendor",
        existing_type=sa.String(length=255),
        type_=postgresql.ENUM("Cisco", name="vendorchoices"),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
