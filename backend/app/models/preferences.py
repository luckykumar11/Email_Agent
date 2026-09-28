from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EmailPreference(Base):
    __tablename__ = "email_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), unique=True, nullable=False)
    sender_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reply_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    default_signature: Mapped[bool] = mapped_column(Boolean, default=True)
    append_signature: Mapped[bool] = mapped_column(Boolean, default=True)
    email_format: Mapped[str] = mapped_column(String(20), default="html")
    default_cc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_bcc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sending_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    company: Mapped["Company"] = relationship("Company", back_populates="email_preferences")
