"""
Pytest configuration and fixtures for CleanoutPro tests
"""

import pytest
from sqlalchemy import create_engine, event, TypeDecorator, String
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import uuid
from datetime import datetime, timedelta
import json

from database.connection import Base, get_db
from database.models import Customer, Job, Room, Invoice, PricingRule
from api.main import app


# SQLite-compatible UUID type
class GUID(TypeDecorator):
    """Platform-independent GUID type for SQLite"""
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


# SQLite-compatible JSONB type
class JSON_SQLite(TypeDecorator):
    """Platform-independent JSON type for SQLite"""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


# Monkey-patch database types for testing
import database.models as models
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB

# Replace PostgreSQL types with SQLite-compatible types
for model_name in dir(models):
    model = getattr(models, model_name)
    if hasattr(model, '__tablename__'):
        for column in model.__table__.columns:
            if isinstance(column.type, PG_UUID):
                column.type = GUID()
            elif isinstance(column.type, PG_JSONB):
                column.type = JSON_SQLite()


# Test database URL (use file-based SQLite for compatibility)
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database for each test function
    Fresh database for each test ensures isolation
    """
    # Create test engine
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}  # SQLite specific
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    FastAPI test client with test database
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_customer(test_db):
    """Create a sample customer for testing"""
    customer = Customer(
        id=uuid.uuid4(),
        name="John Doe",
        email="john@example.com",
        phone="555-0123",
        address="123 Main St, Anytown, USA"
    )
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    return customer


@pytest.fixture
def sample_job(test_db, sample_customer):
    """Create a sample job for testing"""
    job = Job(
        id=uuid.uuid4(),
        customer_id=sample_customer.id,
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-001",
        status="draft",
        property_address="456 Oak Ave, Anytown, USA",
        base_estimate=0.00,
        ai_estimate=0.00,
        human_adjusted_estimate=0.00,
        final_price=0.00
    )
    test_db.add(job)
    test_db.commit()
    test_db.refresh(job)
    return job


@pytest.fixture
def sample_room(test_db, sample_job):
    """Create a sample room for testing"""
    room = Room(
        id=uuid.uuid4(),
        job_id=sample_job.id,
        name="Master Bedroom",
        room_number=1,
        ai_size_class="large",
        ai_workload_class="heavy",
        ai_confidence=0.87,
        ai_reasoning="Large room with significant clutter density",
        ai_features={
            "clutter_density": 0.75,
            "accessibility": "moderate",
            "item_categories": ["furniture", "boxes"]
        },
        final_size_class="large",
        final_workload_class="heavy",
        estimated_cost=468.00
    )
    test_db.add(room)
    test_db.commit()
    test_db.refresh(room)
    return room


@pytest.fixture
def sample_pricing_rules(test_db):
    """Create default pricing rules for testing"""
    rules = [
        # Size multipliers
        PricingRule(
            rule_name="Small Room Base",
            rule_type="size_multiplier",
            size_class="small",
            size_multiplier=1.0
        ),
        PricingRule(
            rule_name="Medium Room Base",
            rule_type="size_multiplier",
            size_class="medium",
            size_multiplier=1.5
        ),
        PricingRule(
            rule_name="Large Room Base",
            rule_type="size_multiplier",
            size_class="large",
            size_multiplier=2.0
        ),
        PricingRule(
            rule_name="Extra Large Room Base",
            rule_type="size_multiplier",
            size_class="extra_large",
            size_multiplier=3.0
        ),

        # Workload multipliers
        PricingRule(
            rule_name="Light Workload",
            rule_type="workload_multiplier",
            workload_class="light",
            workload_multiplier=1.0
        ),
        PricingRule(
            rule_name="Moderate Workload",
            rule_type="workload_multiplier",
            workload_class="moderate",
            workload_multiplier=1.3
        ),
        PricingRule(
            rule_name="Heavy Workload",
            rule_type="workload_multiplier",
            workload_class="heavy",
            workload_multiplier=1.6
        ),
        PricingRule(
            rule_name="Extreme Workload",
            rule_type="workload_multiplier",
            workload_class="extreme",
            workload_multiplier=2.0
        ),

        # Base labor
        PricingRule(
            rule_name="Base Labor Rate",
            rule_type="base_labor",
            flat_fee=150.00
        )
    ]

    for rule in rules:
        test_db.add(rule)
    test_db.commit()

    return rules


@pytest.fixture
def mock_image_data():
    """Mock image data for AI vision testing"""
    # Simple 1x1 pixel PNG (base64 encoded)
    return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'


@pytest.fixture
def mock_ai_classification():
    """Mock AI classification response"""
    return {
        "size_class": "large",
        "workload_class": "heavy",
        "confidence": 0.87,
        "reasoning": "Large room with significant furniture and moderate clutter density. Multiple large items visible.",
        "features": {
            "clutter_density": 0.75,
            "accessibility": "moderate",
            "stairs_required": False,
            "hazmat_present": False,
            "salvage_potential": "medium",
            "item_categories": ["furniture", "boxes", "appliances"]
        },
        "processing_time": 12.5
    }
