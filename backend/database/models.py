"""
SQLAlchemy ORM Models
Maps to PostgreSQL schema
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    jobs = relationship("Job", back_populates="customer")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"))
    job_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), nullable=False, default='draft')
    property_address = Column(Text, nullable=False)
    scheduled_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))

    # Pricing
    base_estimate = Column(DECIMAL(10, 2), default=0.00)
    ai_estimate = Column(DECIMAL(10, 2), default=0.00)
    human_adjusted_estimate = Column(DECIMAL(10, 2), default=0.00)
    final_price = Column(DECIMAL(10, 2), default=0.00)

    # Adjustments
    adjustments = Column(JSONB, default=[])

    # AI metadata
    ai_confidence = Column(Float, default=0.0)
    ai_processing_time = Column(Float, default=0.0)

    notes = Column(Text)
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="jobs")
    rooms = relationship("Room", back_populates="job", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="job")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    room_number = Column(Integer, nullable=False)

    # Image data
    image_url = Column(Text)
    image_path = Column(Text)
    thumbnail_url = Column(Text)

    # AI Classification
    ai_size_class = Column(String(50))
    ai_workload_class = Column(String(50))
    ai_confidence = Column(Float, default=0.0)
    ai_reasoning = Column(Text)
    ai_features = Column(JSONB, default={})

    # Human Overrides
    human_size_class = Column(String(50))
    human_workload_class = Column(String(50))
    human_override_reason = Column(Text)

    # Final Classification
    final_size_class = Column(String(50), nullable=False)
    final_workload_class = Column(String(50), nullable=False)

    # Pricing
    estimated_cost = Column(DECIMAL(10, 2), default=0.00)

    captured_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="rooms")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"))
    invoice_number = Column(String(50), unique=True, nullable=False)

    # Line items
    line_items = Column(JSONB, default=[])

    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_rate = Column(DECIMAL(5, 4), default=0.0000)
    tax_amount = Column(DECIMAL(10, 2), default=0.00)
    total = Column(DECIMAL(10, 2), nullable=False)

    # PayPal
    paypal_payment_id = Column(String(255))
    paypal_payment_status = Column(String(50))
    paypal_payer_email = Column(String(255))

    # Status
    status = Column(String(50), nullable=False, default='draft')

    issued_date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    paid_date = Column(DateTime(timezone=True))

    notes = Column(Text)
    pdf_url = Column(Text)
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="invoices")
    transactions = relationship("PaymentTransaction", back_populates="invoice")


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))

    transaction_type = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)

    # PayPal
    paypal_transaction_id = Column(String(255), unique=True)
    paypal_status = Column(String(50))
    paypal_response = Column(JSONB)

    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="transactions")


class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_name = Column(String(255), nullable=False)
    rule_type = Column(String(50), nullable=False)

    # Multipliers
    size_class = Column(String(50))
    size_multiplier = Column(DECIMAL(5, 2))
    workload_class = Column(String(50))
    workload_multiplier = Column(DECIMAL(5, 2))

    # Flat fees
    flat_fee = Column(DECIMAL(10, 2))

    # Conditions
    condition = Column(JSONB)

    active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    meta_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SyncQueue(Base):
    __tablename__ = "sync_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(50), nullable=False)
    payload = Column(JSONB, nullable=False)
    status = Column(String(50), default='pending')
    retry_count = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(UUID(as_uuid=True))
    changes = Column(JSONB)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
