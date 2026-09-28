"""initial tables

Revision ID: 001_initial
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("industry", sa.String(255), nullable=True),
        sa.Column("location", sa.String(500), nullable=True),
        sa.Column("contact_person", sa.String(255), nullable=True),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(50), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "services_products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "target_customers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "value_propositions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "social_links",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(100), nullable=False),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "email_configurations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("email_address", sa.String(255), nullable=False),
        sa.Column("smtp_host", sa.String(255), nullable=False),
        sa.Column("smtp_port", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("encrypted_password", sa.String(500), nullable=False),
        sa.Column("security_type", sa.String(20), nullable=False),
        sa.Column("sender_name", sa.String(255), nullable=True),
        sa.Column("reply_to", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id"),
    )

    op.create_table(
        "email_signatures",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("signature_text", sa.Text(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("append_automatically", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id"),
    )

    op.create_table(
        "email_preferences",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("sender_name", sa.String(255), nullable=True),
        sa.Column("reply_to", sa.String(255), nullable=True),
        sa.Column("default_signature", sa.Boolean(), nullable=True),
        sa.Column("append_signature", sa.Boolean(), nullable=True),
        sa.Column("email_format", sa.String(20), nullable=True),
        sa.Column("default_cc", sa.Text(), nullable=True),
        sa.Column("default_bcc", sa.Text(), nullable=True),
        sa.Column("sending_limit", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id"),
    )

    op.create_table(
        "email_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("sender", sa.String(255), nullable=False),
        sa.Column("recipient", sa.String(255), nullable=False),
        sa.Column("cc", sa.Text(), nullable=True),
        sa.Column("bcc", sa.Text(), nullable=True),
        sa.Column("subject", sa.String(500), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("format", sa.String(20), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_email_history_company_id", "email_history", ["company_id"])


def downgrade() -> None:
    op.drop_table("email_history")
    op.drop_table("email_preferences")
    op.drop_table("email_signatures")
    op.drop_table("email_configurations")
    op.drop_table("social_links")
    op.drop_table("value_propositions")
    op.drop_table("target_customers")
    op.drop_table("services_products")
    op.drop_table("companies")
    op.drop_index("ix_users_email")
    op.drop_table("users")
