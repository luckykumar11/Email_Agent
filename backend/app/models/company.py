from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    contact_person: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship("User", back_populates="company")
    services_products: Mapped[List["ServiceProduct"]] = relationship(
        "ServiceProduct", back_populates="company", cascade="all, delete-orphan"
    )
    target_customers: Mapped[List["TargetCustomer"]] = relationship(
        "TargetCustomer", back_populates="company", cascade="all, delete-orphan"
    )
    value_propositions: Mapped[List["ValueProposition"]] = relationship(
        "ValueProposition", back_populates="company", cascade="all, delete-orphan"
    )
    social_links: Mapped[List["SocialLink"]] = relationship(
        "SocialLink", back_populates="company", cascade="all, delete-orphan"
    )
    email_config: Mapped[Optional["EmailConfiguration"]] = relationship(
        "EmailConfiguration", back_populates="company", uselist=False, cascade="all, delete-orphan"
    )
    email_signature: Mapped[Optional["EmailSignature"]] = relationship(
        "EmailSignature", back_populates="company", uselist=False, cascade="all, delete-orphan"
    )
    email_preferences: Mapped[Optional["EmailPreference"]] = relationship(
        "EmailPreference", back_populates="company", uselist=False, cascade="all, delete-orphan"
    )
    email_history: Mapped[List["EmailHistory"]] = relationship(
        "EmailHistory", back_populates="company", cascade="all, delete-orphan"
    )


class ServiceProduct(Base):
    __tablename__ = "services_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    company: Mapped["Company"] = relationship("Company", back_populates="services_products")


class TargetCustomer(Base):
    __tablename__ = "target_customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    company: Mapped["Company"] = relationship("Company", back_populates="target_customers")


class ValueProposition(Base):
    __tablename__ = "value_propositions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    company: Mapped["Company"] = relationship("Company", back_populates="value_propositions")


class SocialLink(Base):
    __tablename__ = "social_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=False)
    platform: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    company: Mapped["Company"] = relationship("Company", back_populates="social_links")
