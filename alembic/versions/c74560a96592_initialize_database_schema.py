"""Initialize Database Schema

Revision ID: c74560a96592
Revises: 
Create Date: 2024-04-26 22:01:37.653435

"""

import uuid
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy import VARCHAR
from sqlalchemy.types import UUID
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PasswordType
from sqlalchemy_utils import TimezoneType

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c74560a96592"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("username", VARCHAR(128), nullable=False, unique=True),
        sa.Column("email", EmailType, nullable=False, unique=True),
        sa.Column("password", PasswordType, nullable=False),
        sa.Column("created_at", TimezoneType, nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "groups",
        sa.Column("group_id", UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("group_name", sa.String(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("group_id"),
    )

    op.create_table(
        "group_users",
        sa.Column("group_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.group_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("group_id", "user_id"),
    )

    op.create_table(
        "expense",
        sa.Column("expense_id", UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("group_id", sa.String(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["group_id"], ["groups.group_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("expense_id"),
    )

    op.create_table(
        "split",
        sa.Column("split_id", UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("expense_id", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("group_id", sa.String(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["expense_id"], ["expense.expense_id"]),
        sa.ForeignKeyConstraint(["group_id"], ["groups.group_id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("split_id"),
    )


def downgrade():
    op.drop_table("split")
    op.drop_table("expense")
    op.drop_table("group_users")
    op.drop_table("groups")
    op.drop_table("users")
