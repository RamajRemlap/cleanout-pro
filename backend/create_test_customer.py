"""
Create a test customer in the database
Run this to have a customer ID for testing job creation
"""

import uuid
from datetime import datetime
from database.connection import SessionLocal
from database.models import Customer

def create_test_customer():
    """Create a test customer for API testing"""
    db = SessionLocal()

    try:
        # Check if test customer already exists
        existing = db.query(Customer).filter(Customer.email == "test@cleanoutpro.com").first()

        if existing:
            print("="*60)
            print("TEST CUSTOMER ALREADY EXISTS")
            print("="*60)
            print(f"\nCustomer ID: {existing.id}")
            print(f"Name: {existing.name}")
            print(f"Email: {existing.email}")
            print(f"Phone: {existing.phone}")
            print(f"Address: {existing.address}")
            print("\n" + "="*60)
            print("Use this customer ID to create jobs!")
            print("="*60)
            return str(existing.id)

        # Create new test customer
        customer = Customer(
            id=uuid.uuid4(),
            name="John Doe (Test Customer)",
            email="test@cleanoutpro.com",
            phone="555-0123",
            address="123 Test Street, Anytown, USA 12345"
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        print("="*60)
        print("TEST CUSTOMER CREATED SUCCESSFULLY")
        print("="*60)
        print(f"\nCustomer ID: {customer.id}")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")
        print(f"Phone: {customer.phone}")
        print(f"Address: {customer.address}")
        print(f"\nCreated at: {customer.created_at}")
        print("\n" + "="*60)
        print("COPY THIS CUSTOMER ID FOR API TESTING:")
        print("="*60)
        print(f"\n{customer.id}\n")
        print("="*60)
        print("Use this ID when creating jobs via API")
        print("="*60)

        return str(customer.id)

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Failed to create customer: {e}")
        return None

    finally:
        db.close()

if __name__ == "__main__":
    create_test_customer()
