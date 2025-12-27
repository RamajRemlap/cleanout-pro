"""
Comprehensive Test Data Seeder for CleanoutPro
Creates realistic customers, jobs, rooms, and pricing scenarios
NO MOCK DATA - Real business scenarios for testing
"""

import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from database.connection import SessionLocal
from database.models import Customer, Job, Room, PricingRule
from services.pricing_engine import PricingEngine

def clear_existing_data(db):
    """Clear existing test data (optional)"""
    print("\n[CLEANUP] Clearing existing data...")

    # Delete in correct order (respecting foreign keys)
    db.query(Room).delete()
    db.query(Job).delete()
    db.query(Customer).delete()

    db.commit()
    print("[OK] Existing data cleared")

def seed_customers(db):
    """Create realistic customers"""
    print("\n[SEED] Creating customers...")

    customers_data = [
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "555-0101",
            "address": "1234 Maple Street, Springfield, IL 62701"
        },
        {
            "name": "Michael Chen",
            "email": "m.chen@business.com",
            "phone": "555-0102",
            "address": "5678 Oak Avenue, Portland, OR 97201"
        },
        {
            "name": "Estate of Robert Williams",
            "email": "executor@williams-estate.com",
            "phone": "555-0103",
            "address": "9012 Pine Road, Austin, TX 78701"
        },
        {
            "name": "Green Valley Property Management",
            "email": "contact@greenvalley.com",
            "phone": "555-0104",
            "address": "3456 Business Park Drive, Denver, CO 80202"
        },
        {
            "name": "Jennifer Martinez",
            "email": "jennifer.martinez@gmail.com",
            "phone": "555-0105",
            "address": "7890 Elm Street, Seattle, WA 98101"
        }
    ]

    customers = []
    for data in customers_data:
        customer = Customer(
            id=uuid.uuid4(),
            **data
        )
        db.add(customer)
        customers.append(customer)

    db.commit()

    for customer in customers:
        db.refresh(customer)

    print(f"[OK] Created {len(customers)} customers")
    return customers

def seed_jobs_and_rooms(db, customers):
    """Create realistic jobs with rooms"""
    print("\n[SEED] Creating jobs and rooms...")

    pricing_engine = PricingEngine()

    # Scenario 1: Estate Cleanout (Complete House)
    job1 = Job(
        id=uuid.uuid4(),
        customer_id=customers[2].id,  # Estate of Robert Williams
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-001",
        status="estimated",
        property_address="9012 Pine Road, Austin, TX 78701",
        scheduled_date=datetime.now() + timedelta(days=7),
        notes="Complete estate cleanout. Deceased owner, family wants everything removed except flagged items.",
        adjustments=[
            {"type": "bin_rental", "description": "30-yard dumpster", "amount": 300.00},
            {"type": "stairs", "description": "2 flights of stairs", "amount": 50.00}
        ]
    )
    db.add(job1)

    # Job 1 Rooms
    rooms_job1 = [
        {
            "name": "Master Bedroom",
            "room_number": 1,
            "ai_size_class": "large",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.89,
            "ai_reasoning": "Large bedroom with extensive personal belongings, clothing, and furniture. High clutter density visible.",
            "ai_features": {
                "clutter_density": 0.82,
                "accessibility": "moderate",
                "item_categories": ["furniture", "boxes", "clothing", "personal_items"],
                "salvage_potential": "low"
            }
        },
        {
            "name": "Living Room",
            "room_number": 2,
            "ai_size_class": "large",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.85,
            "ai_reasoning": "Spacious living area with standard furniture. Moderate amount of items to remove.",
            "ai_features": {
                "clutter_density": 0.55,
                "accessibility": "easy",
                "item_categories": ["furniture", "electronics", "decorations"],
                "salvage_potential": "medium"
            }
        },
        {
            "name": "Garage",
            "room_number": 3,
            "ai_size_class": "extra_large",
            "ai_workload_class": "extreme",
            "ai_confidence": 0.92,
            "ai_reasoning": "Very large garage packed with decades of accumulated items. Difficult access, heavy items, tools, and equipment.",
            "ai_features": {
                "clutter_density": 0.95,
                "accessibility": "difficult",
                "item_categories": ["tools", "equipment", "boxes", "furniture", "appliances"],
                "salvage_potential": "high",
                "hazmat_present": True
            },
            "human_size_class": "extra_large",
            "human_workload_class": "extreme",
            "human_override_reason": "Confirmed on-site. Hazmat items identified (old paint, chemicals)."
        },
        {
            "name": "Kitchen",
            "room_number": 4,
            "ai_size_class": "medium",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.88,
            "ai_reasoning": "Standard kitchen with appliances and cabinets full of items.",
            "ai_features": {
                "clutter_density": 0.65,
                "accessibility": "easy",
                "item_categories": ["appliances", "kitchenware", "furniture"],
                "salvage_potential": "low"
            }
        },
        {
            "name": "Basement",
            "room_number": 5,
            "ai_size_class": "extra_large",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.87,
            "ai_reasoning": "Large basement storage area with boxes, old furniture, and miscellaneous items.",
            "ai_features": {
                "clutter_density": 0.75,
                "accessibility": "difficult",
                "stairs_required": True,
                "item_categories": ["boxes", "furniture", "storage_items"],
                "salvage_potential": "medium"
            }
        }
    ]

    # Scenario 2: Apartment Turnover (Property Management)
    job2 = Job(
        id=uuid.uuid4(),
        customer_id=customers[3].id,  # Green Valley Property Management
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-002",
        status="approved",
        property_address="Unit 4B, 3456 Business Park Drive, Denver, CO 80202",
        scheduled_date=datetime.now() + timedelta(days=3),
        notes="Tenant left behind items. Need unit cleared for new tenant move-in next week.",
        adjustments=[
            {"type": "bin_rental", "description": "20-yard dumpster", "amount": 200.00}
        ]
    )
    db.add(job2)

    # Job 2 Rooms
    rooms_job2 = [
        {
            "name": "Bedroom",
            "room_number": 1,
            "ai_size_class": "medium",
            "ai_workload_class": "light",
            "ai_confidence": 0.91,
            "ai_reasoning": "Standard bedroom, mostly empty with a few abandoned items.",
            "ai_features": {
                "clutter_density": 0.25,
                "accessibility": "easy",
                "item_categories": ["furniture", "boxes"],
                "salvage_potential": "none"
            }
        },
        {
            "name": "Living/Dining",
            "room_number": 2,
            "ai_size_class": "medium",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.86,
            "ai_reasoning": "Open floor plan with some furniture and boxes left behind.",
            "ai_features": {
                "clutter_density": 0.45,
                "accessibility": "easy",
                "item_categories": ["furniture", "boxes", "miscellaneous"],
                "salvage_potential": "low"
            }
        }
    ]

    # Scenario 3: Downsizing Senior Move
    job3 = Job(
        id=uuid.uuid4(),
        customer_id=customers[0].id,  # Sarah Johnson
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-003",
        status="estimated",
        property_address="1234 Maple Street, Springfield, IL 62701",
        scheduled_date=datetime.now() + timedelta(days=14),
        notes="Senior moving to assisted living. Keeping minimal items, removing most furniture and belongings.",
        adjustments=[
            {"type": "bin_rental", "description": "20-yard dumpster", "amount": 200.00},
            {"type": "donation", "description": "Donation delivery to Goodwill", "amount": 75.00}
        ]
    )
    db.add(job3)

    # Job 3 Rooms
    rooms_job3 = [
        {
            "name": "Bedroom 1",
            "room_number": 1,
            "ai_size_class": "medium",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.84,
            "ai_reasoning": "Bedroom with furniture and personal items to be removed.",
            "ai_features": {
                "clutter_density": 0.60,
                "accessibility": "easy",
                "item_categories": ["furniture", "clothing", "personal_items"],
                "salvage_potential": "high"
            },
            "human_size_class": "medium",
            "human_workload_class": "light",
            "human_override_reason": "Client is keeping bed and dresser. Only removing smaller items."
        },
        {
            "name": "Bedroom 2 / Office",
            "room_number": 2,
            "ai_size_class": "small",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.79,
            "ai_reasoning": "Small room packed with papers, books, and office equipment.",
            "ai_features": {
                "clutter_density": 0.85,
                "accessibility": "moderate",
                "item_categories": ["books", "papers", "office_equipment"],
                "salvage_potential": "medium"
            }
        },
        {
            "name": "Attic",
            "room_number": 3,
            "ai_size_class": "large",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.81,
            "ai_reasoning": "Attic storage with decades of accumulated items, boxes, and holiday decorations.",
            "ai_features": {
                "clutter_density": 0.78,
                "accessibility": "difficult",
                "stairs_required": True,
                "item_categories": ["boxes", "decorations", "storage_items"],
                "salvage_potential": "medium"
            }
        }
    ]

    # Scenario 4: Garage-Only Cleanout
    job4 = Job(
        id=uuid.uuid4(),
        customer_id=customers[1].id,  # Michael Chen
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-004",
        status="completed",
        property_address="5678 Oak Avenue, Portland, OR 97201",
        scheduled_date=datetime.now() - timedelta(days=2),
        completed_date=datetime.now() - timedelta(days=1),
        notes="Garage cleanout for home sale preparation. Quick turnaround needed.",
        adjustments=[
            {"type": "bin_rental", "description": "20-yard dumpster", "amount": 200.00}
        ]
    )
    db.add(job4)

    # Job 4 Rooms
    rooms_job4 = [
        {
            "name": "2-Car Garage",
            "room_number": 1,
            "ai_size_class": "large",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.88,
            "ai_reasoning": "Two-car garage with typical accumulated items and storage boxes.",
            "ai_features": {
                "clutter_density": 0.65,
                "accessibility": "easy",
                "item_categories": ["boxes", "tools", "sports_equipment", "seasonal_items"],
                "salvage_potential": "medium"
            }
        }
    ]

    # Scenario 5: Hoarding Situation
    job5 = Job(
        id=uuid.uuid4(),
        customer_id=customers[4].id,  # Jennifer Martinez
        job_number=f"JOB-{datetime.now().strftime('%Y%m%d')}-005",
        status="draft",
        property_address="7890 Elm Street, Seattle, WA 98101",
        notes="Hoarding cleanup. Require specialized handling and disposal. Biohazard potential.",
        adjustments=[
            {"type": "bin_rental", "description": "30-yard dumpster", "amount": 300.00},
            {"type": "hazmat", "description": "Biohazard handling and disposal", "amount": 150.00},
            {"type": "access", "description": "Difficult access - narrow hallways", "amount": 75.00}
        ]
    )
    db.add(job5)

    # Job 5 Rooms
    rooms_job5 = [
        {
            "name": "Living Room",
            "room_number": 1,
            "ai_size_class": "large",
            "ai_workload_class": "extreme",
            "ai_confidence": 0.94,
            "ai_reasoning": "Severe hoarding situation. Floor-to-ceiling clutter, difficult pathways, potential biohazards.",
            "ai_features": {
                "clutter_density": 0.98,
                "accessibility": "difficult",
                "hazmat_present": True,
                "item_categories": ["miscellaneous", "trash", "boxes", "furniture"],
                "salvage_potential": "none"
            }
        },
        {
            "name": "Kitchen",
            "room_number": 2,
            "ai_size_class": "medium",
            "ai_workload_class": "extreme",
            "ai_confidence": 0.96,
            "ai_reasoning": "Kitchen with extreme clutter, food waste, potential health hazards.",
            "ai_features": {
                "clutter_density": 0.95,
                "accessibility": "difficult",
                "hazmat_present": True,
                "item_categories": ["trash", "food_waste", "miscellaneous"],
                "salvage_potential": "none"
            }
        }
    ]

    # Create all rooms and calculate pricing
    all_rooms_data = [
        (job1, rooms_job1),
        (job2, rooms_job2),
        (job3, rooms_job3),
        (job4, rooms_job4),
        (job5, rooms_job5)
    ]

    total_rooms = 0
    for job, rooms_data in all_rooms_data:
        job_rooms = []

        for room_data in rooms_data:
            # Determine final classification
            final_size = room_data.get('human_size_class') or room_data['ai_size_class']
            final_workload = room_data.get('human_workload_class') or room_data['ai_workload_class']

            # Calculate cost
            estimated_cost = pricing_engine.calculate_room_cost(final_size, final_workload)

            room = Room(
                id=uuid.uuid4(),
                job_id=job.id,
                final_size_class=final_size,
                final_workload_class=final_workload,
                estimated_cost=estimated_cost,
                captured_at=datetime.now() - timedelta(days=1),
                processed_at=datetime.now(),
                **room_data
            )
            db.add(room)
            job_rooms.append(room)
            total_rooms += 1

        # Calculate job totals
        rooms_total = sum(float(r.estimated_cost) for r in job_rooms)
        adjustments_total = sum(float(adj['amount']) for adj in (job.adjustments or []))

        job.ai_estimate = Decimal(str(rooms_total))
        job.base_estimate = Decimal(str(rooms_total))
        job.final_price = Decimal(str(rooms_total + adjustments_total))

    db.commit()

    print(f"[OK] Created 5 jobs with {total_rooms} rooms total")

    # Print summary
    print("\n" + "="*60)
    print("JOB SUMMARY")
    print("="*60)

    for job, rooms_data in all_rooms_data:
        db.refresh(job)
        print(f"\n{job.job_number} - {job.status.upper()}")
        print(f"  Customer: {[c for c in customers if c.id == job.customer_id][0].name}")
        print(f"  Address: {job.property_address}")
        print(f"  Rooms: {len(rooms_data)}")
        print(f"  AI Estimate: ${float(job.ai_estimate):.2f}")
        print(f"  Final Price: ${float(job.final_price):.2f}")
        print(f"  Status: {job.status}")

def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("CLEANOUTPRO COMPREHENSIVE TEST DATA SEEDER")
    print("="*60)

    db = SessionLocal()

    try:
        # Clear existing data
        clear_existing_data(db)

        # Seed customers
        customers = seed_customers(db)

        # Seed jobs and rooms
        seed_jobs_and_rooms(db, customers)

        print("\n" + "="*60)
        print("[SUCCESS] TEST DATA SEEDING COMPLETE")
        print("="*60)
        print("\nDatabase now contains:")
        print("  - 5 Customers (realistic scenarios)")
        print("  - 5 Jobs (various statuses and complexities)")
        print("  - 15 Rooms (with AI classifications and pricing)")
        print("  - Real pricing calculations")
        print("  - Human overrides demonstrated")
        print("\n" + "="*60)
        print("READY FOR API TESTING")
        print("="*60)
        print("\nNext steps:")
        print("  1. Start API server: python api/main.py")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Test all endpoints with real data!")
        print("="*60 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    main()
