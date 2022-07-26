"""updated models

Revision ID: 0e7ad884be1e
Revises: ac177b4eb4af
Create Date: 2022-07-25 13:08:31.663453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0e7ad884be1e"
down_revision = "ac177b4eb4af"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("devices", sa.Column("host", sa.String(length=255), nullable=True))
    op.drop_column("devices", "vendor")
    op.drop_column("devices", "fqdn")
    op.drop_column("devices", "model")
    op.drop_column("devices", "operating_system")
    op.drop_column("devices", "site")
    op.drop_column("devices", "os_version")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "devices",
        sa.Column(
            "os_version", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "devices",
        sa.Column("site", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    )
    op.add_column(
        "devices",
        sa.Column(
            "operating_system",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "devices",
        sa.Column("model", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    )
    op.add_column(
        "devices",
        sa.Column("fqdn", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    )
    op.add_column(
        "devices",
        sa.Column("vendor", sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    )
    op.drop_column("devices", "host")
    # ### end Alembic commands ###
