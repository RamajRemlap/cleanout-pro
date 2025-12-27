"""
Create test data for CleanoutPro API
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.connection import SessionLocal, init_db, engine
from database.models import Customer, Job, Room, PricingRule
from services.pricing_engine import PricingEngine
import uuid


def wait_for_db(max_attempts=30, delay=2):
    """Wait for database to be ready"""
    import time
    from sqlalchemy import text

    print("Waiting for database connection...")
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("[OK] Database is ready!")
            return True
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"  Attempt {attempt + 1}/{max_attempts}: Waiting for database... ({e})")
                time.sleep(delay)
            else:
                print(f"[FAIL] Database not ready after {max_attempts} attempts")
                return False
    return False


def create_tables():
    """Create all database tables"""
    print("\nCreating database tables...")
    try:
        init_db()
        print("[OK] All tables created successfully!")
        return True
    except Exception as e:
        print(f"[FAIL] Error creating tables: {e}")
        return False


def create_pricing_rules(db):
    """Create default pricing rules"""
    print("\nCreating pricing rules...")

    # Check if rules already exist
    existing = db.query(PricingRule).count()
    if existing > 0:
        print(f"  [SKIP] {existing} pricing rules already exist")
        return

    rules = [
        {
            "rule_name": "Small Room Base",
            "rule_type": "size_multiplier",
            "size_class": "small",
            "size_multiplier": Decimal("1.0"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Medium Room Base",
            "rule_type": "size_multiplier",
            "size_class": "medium",
            "size_multiplier": Decimal("1.5"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Large Room Base",
            "rule_type": "size_multiplier",
            "size_class": "large",
            "size_multiplier": Decimal("2.0"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Extra Large Room Base",
            "rule_type": "size_multiplier",
            "size_class": "extra_large",
            "size_multiplier": Decimal("3.0"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Light Workload",
            "rule_type": "workload_multiplier",
            "workload_class": "light",
            "workload_multiplier": Decimal("1.0"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Moderate Workload",
            "rule_type": "workload_multiplier",
            "workload_class": "moderate",
            "workload_multiplier": Decimal("1.3"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Heavy Workload",
            "rule_type": "workload_multiplier",
            "workload_class": "heavy",
            "workload_multiplier": Decimal("1.6"),
            "active": True,
            "priority": 1
        },
        {
            "rule_name": "Extreme Workload",
            "rule_type": "workload_multiplier",
            "workload_class": "extreme",
            "workload_multiplier": Decimal("2.0"),
            "active": True,
            "priority": 1
        }
    ]

    for rule_data in rules:
        rule = PricingRule(**rule_data)
        db.add(rule)

    db.commit()
    print(f"[OK] Created {len(rules)} pricing rules")


def create_test_customers(db):
    """Create test customers"""
    print("\nCreating test customers...")

    # Check if customers already exist
    existing = db.query(Customer).count()
    if existing > 0:
        print(f"  [SKIP] {existing} customers already exist")
        return db.query(Customer).all()

    customers_data = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "phone": "(555) 123-4567",
            "address": "123 Main St, Springfield, IL 62701"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.j@example.com",
            "phone": "(555) 234-5678",
            "address": "456 Oak Ave, Springfield, IL 62702"
        },
        {
            "name": "Michael Davis",
            "email": "m.davis@example.com",
            "phone": "(555) 345-6789",
            "address": "789 Elm Street, Springfield, IL 62703"
        }
    ]

    customers = []
    for customer_data in customers_data:
        customer = Customer(**customer_data)
        db.add(customer)
        customers.append(customer)

    db.commit()

    # Refresh to get IDs
    for customer in customers:
        db.refresh(customer)

    print(f"[OK] Created {len(customers)} customers")
    return customers


def create_test_jobs(db, customers):
    """Create test jobs"""
    print("\nCreating test jobs...")

    # Check if jobs already exist
    existing = db.query(Job).count()
    if existing > 0:
        print(f"  [SKIP] {existing} jobs already exist")
        return db.query(Job).all()

    jobs_data = [
        {
            "customer_id": customers[0].id,
            "job_number": f"JOB-{int(datetime.now().timestamp())}",
            "property_address": customers[0].address,
            "scheduled_date": datetime.now() + timedelta(days=3),
            "status": "estimated",
            "notes": "Whole house cleanout - customer moving to Florida"
        },
        {
            "customer_id": customers[1].id,
            "job_number": f"JOB-{int(datetime.now().timestamp()) + 1}",
            "property_address": "789 Storage Unit Rd, Springfield, IL 62704",
            "scheduled_date": datetime.now() + timedelta(days=7),
            "status": "draft",
            "notes": "Storage unit cleanout - inherited items"
        },
        {
            "customer_id": customers[2].id,
            "job_number": f"JOB-{int(datetime.now().timestamp()) + 2}",
            "property_address": customers[2].address,
            "scheduled_date": datetime.now() + timedelta(days=1),
            "status": "approved",
            "notes": "Garage and basement only - keep antiques separate"
        }
    ]

    jobs = []
    for job_data in jobs_data:
        job = Job(**job_data)
        db.add(job)
        jobs.append(job)

    db.commit()

    # Refresh to get IDs
    for job in jobs:
        db.refresh(job)

    print(f"[OK] Created {len(jobs)} jobs")
    return jobs


def create_test_rooms(db, jobs):
    """Create test rooms with AI classifications"""
    print("\nCreating test rooms...")

    # Check if rooms already exist
    existing = db.query(Room).count()
    if existing > 0:
        print(f"  [SKIP] {existing} rooms already exist")
        return

    pricing_engine = PricingEngine()

    # Job 1 rooms (whole house cleanout)
    job1_rooms = [
        {
            "name": "Master Bedroom",
            "room_number": 1,
            "ai_size_class": "large",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.92,
            "ai_reasoning": "Large bedroom approximately 15x12 feet. Moderate clutter with furniture, boxes, and personal items. Standard accessibility.",
            "ai_features": {
                "clutter_density": 0.6,
                "accessibility": "moderate",
                "item_categories": ["furniture", "boxes", "clothing"]
            }
        },
        {
            "name": "Living Room",
            "room_number": 2,
            "ai_size_class": "extra_large",
            "ai_workload_class": "light",
            "ai_confidence": 0.88,
            "ai_reasoning": "Extra large living space approximately 20x18 feet. Light clutter, mostly furniture removal. Good accessibility.",
            "ai_features": {
                "clutter_density": 0.3,
                "accessibility": "easy",
                "item_categories": ["furniture", "electronics"]
            }
        },
        {
            "name": "Garage",
            "room_number": 3,
            "ai_size_class": "extra_large",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.85,
            "ai_reasoning": "Two-car garage packed with 40+ years of storage. Heavy workload due to quantity and organization needed.",
            "ai_features": {
                "clutter_density": 0.9,
                "accessibility": "difficult",
                "item_categories": ["tools", "boxes", "yard equipment", "furniture"]
            },
            "human_size_class": "extra_large",
            "human_workload_class": "extreme",
            "human_override_reason": "Customer revealed garage has floor-to-ceiling storage and requires hazmat disposal for old paint cans"
        }
    ]

    # Job 2 rooms (storage unit)
    job2_rooms = [
        {
            "name": "Storage Unit 10x20",
            "room_number": 1,
            "ai_size_class": "medium",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.90,
            "ai_reasoning": "Standard 10x20 storage unit, moderately packed. Mix of furniture and boxes.",
            "ai_features": {
                "clutter_density": 0.7,
                "accessibility": "moderate",
                "item_categories": ["furniture", "boxes", "antiques"]
            }
        }
    ]

    # Job 3 rooms (garage and basement)
    job3_rooms = [
        {
            "name": "Basement",
            "room_number": 1,
            "ai_size_class": "large",
            "ai_workload_class": "heavy",
            "ai_confidence": 0.87,
            "ai_reasoning": "Full basement approximately 30x20 feet. Heavy clutter with limited accessibility due to stairs.",
            "ai_features": {
                "clutter_density": 0.8,
                "accessibility": "difficult",
                "stairs_required": True,
                "item_categories": ["boxes", "furniture", "appliances"]
            }
        },
        {
            "name": "Garage",
            "room_number": 2,
            "ai_size_class": "large",
            "ai_workload_class": "moderate",
            "ai_confidence": 0.91,
            "ai_reasoning": "Single-car garage with moderate storage. Well-organized but needs clearing.",
            "ai_features": {
                "clutter_density": 0.5,
                "accessibility": "moderate",
                "item_categories": ["tools", "sports equipment", "boxes"]
            }
        }
    ]

    # Create rooms for each job
    room_sets = [
        (jobs[0], job1_rooms),
        (jobs[1], job2_rooms),
        (jobs[2], job3_rooms)
    ]

    total_rooms = 0
    for job, room_data_list in room_sets:
        for room_data in room_data_list:
            # Set final classification (human override or AI)
            room_data['final_size_class'] = room_data.get('human_size_class', room_data['ai_size_class'])
            room_data['final_workload_class'] = room_data.get('human_workload_class', room_data['ai_workload_class'])

            # Calculate pricing
            estimated_cost = pricing_engine.calculate_room_cost(
                room_data['final_size_class'],
                room_data['final_workload_class']
            )
            room_data['estimated_cost'] = estimated_cost

            # Add job reference
            room_data['job_id'] = job.id
            room_data['processed_at'] = datetime.now()

            room = Room(**room_data)
            db.add(room)
            total_rooms += 1

    db.commit()
    print(f"[OK] Created {total_rooms} rooms across {len(jobs)} jobs")

    # Update job estimates
    print("\nUpdating job estimates...")
    for job in jobs:
        job_rooms = db.query(Room).filter(Room.job_id == job.id).all()

        # Calculate AI estimate (sum of AI classifications)
        ai_total = sum(
            float(pricing_engine.calculate_room_cost(r.ai_size_class, r.ai_workload_class))
            for r in job_rooms
        )
        job.ai_estimate = Decimal(str(ai_total))

        # Calculate final price (sum of final classifications with human overrides)
        final_total = sum(float(r.estimated_cost) for r in job_rooms)
        job.final_price = Decimal(str(final_total))

        print(f"  Job {job.job_number}: AI=${ai_total:.2f}, Final=${final_total:.2f}")

    db.commit()
    print("[OK] Job estimates updated")


def print_summary(db):
    """Print summary of created data"""
    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)

    customer_count = db.query(Customer).count()
    job_count = db.query(Job).count()
    room_count = db.query(Room).count()
    rule_count = db.query(PricingRule).count()

    print(f"\nCustomers: {customer_count}")
    print(f"Jobs: {job_count}")
    print(f"Rooms: {room_count}")
    print(f"Pricing Rules: {rule_count}")

    print("\nJobs Details:")
    jobs = db.query(Job).all()
    for job in jobs:
        rooms = db.query(Room).filter(Room.job_id == job.id).all()
        print(f"\n  {job.job_number} ({job.status})")
        print(f"    Customer: {job.customer.name}")
        print(f"    Rooms: {len(rooms)}")
        print(f"    AI Estimate: ${float(job.ai_estimate):.2f}")
        print(f"    Final Price: ${float(job.final_price):.2f}")

        for room in rooms:
            override_marker = " [HUMAN OVERRIDE]" if room.human_size_class else ""
            print(f"      - {room.name}: {room.final_size_class}/{room.final_workload_class} = ${float(room.estimated_cost):.2f}{override_marker}")

    print("\n" + "=" * 60)
    print("TEST DATA CREATION COMPLETE!")
    print("=" * 60)
    print("\nAPI is ready to test at: http://localhost:8001/docs")
    print("\nTry these endpoints:")
    print("  GET  /api/jobs                    - List all jobs")
    print("  GET  /api/jobs/{job_id}          - Get job details")
    print("  GET  /api/jobs/{job_id}/estimate - Get pricing breakdown")
    print("  GET  /api/rooms?job_id={job_id}  - List rooms for a job")
    print()


def main():
    """Main execution"""
    print("=" * 60)
    print("CleanoutPro - Test Data Creation")
    print("=" * 60)

    # Wait for database
    if not wait_for_db():
        print("\n[FAIL] Could not connect to database")
        print("Make sure PostgreSQL is running:")
        print("  docker-compose up -d")
        print("  OR")
        print("  docker run -d --name cleanout-postgres -e POSTGRES_DB=cleanoutpro -e POSTGRES_USER=cleanout -e POSTGRES_PASSWORD=cleanout_dev_password -p 5432:5432 postgres:15")
        return 1

    # Create tables
    if not create_tables():
        return 1

    # Create test data
    db = SessionLocal()
    try:
        create_pricing_rules(db)
        customers = create_test_customers(db)
        jobs = create_test_jobs(db, customers)
        create_test_rooms(db, jobs)

        print_summary(db)

        return 0
    except Exception as e:
        print(f"\n[FAIL] Error creating test data: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
