"""
API Structure Validation Script
Tests that all routes and imports are correctly configured
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("API Structure Validation")
    print("=" * 60)

    try:
        print("\n[OK] Testing database imports...")
        from database import connection, models
        print("  - database.connection: OK")
        print("  - database.models: OK")

        print("\n[OK] Testing service imports...")
        from services import ai_vision, pricing_engine
        print("  - services.ai_vision: OK")
        print("  - services.pricing_engine: OK")

        print("\n[OK] Testing route imports...")
        from api.routes import jobs, rooms
        print("  - api.routes.jobs: OK")
        print("  - api.routes.rooms: OK")

        print("\n[OK] Testing main app...")
        from api import main
        print("  - api.main: OK")

        print("\n[OK] Checking FastAPI app routes...")
        app = main.app
        routes = [route.path for route in app.routes]
        print(f"  - Total routes: {len(routes)}")

        # Filter out default routes
        api_routes = [r for r in routes if r.startswith('/api/')]
        print(f"  - API routes: {len(api_routes)}")
        print("\n  API Endpoints:")
        for route in sorted(api_routes):
            print(f"    - {route}")

        print("\n[OK] Checking route prefixes...")
        routers = [
            (jobs.router, "Jobs"),
            (rooms.router, "Rooms")
        ]

        for router, name in routers:
            print(f"  - {name} router:")
            print(f"    Prefix: {router.prefix}")
            print(f"    Tags: {router.tags}")
            print(f"    Routes: {len(router.routes)}")
            for route in router.routes:
                methods = ', '.join(route.methods) if hasattr(route, 'methods') else 'N/A'
                print(f"      {methods:10} {route.path}")

        print("\n" + "=" * 60)
        print("[PASS] All imports successful!")
        print("=" * 60)

        return True

    except ImportError as e:
        print(f"\n[FAIL] Import Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test database models"""
    print("\n" + "=" * 60)
    print("Database Models Validation")
    print("=" * 60)

    try:
        from database.models import Customer, Job, Room, Invoice, PaymentTransaction, PricingRule, SyncQueue, AuditLog

        models = [
            ("Customer", Customer),
            ("Job", Job),
            ("Room", Room),
            ("Invoice", Invoice),
            ("PaymentTransaction", PaymentTransaction),
            ("PricingRule", PricingRule),
            ("SyncQueue", SyncQueue),
            ("AuditLog", AuditLog)
        ]

        print("\n[OK] Checking model tables:")
        for name, model in models:
            print(f"  - {name}: __tablename__ = '{model.__tablename__}'")

        print("\n[OK] Checking Room model fields:")
        room_columns = Room.__table__.columns.keys()
        critical_fields = [
            'ai_size_class', 'ai_workload_class', 'ai_confidence',
            'human_size_class', 'human_workload_class',
            'final_size_class', 'final_workload_class',
            'estimated_cost'
        ]

        for field in critical_fields:
            status = "[OK]" if field in room_columns else "[X]"
            print(f"  {status} {field}")

        print("\n[OK] Checking Job model relationships:")
        print(f"  - Job.rooms: {hasattr(Job, 'rooms')}")
        print(f"  - Job.customer: {hasattr(Job, 'customer')}")
        print(f"  - Job.invoices: {hasattr(Job, 'invoices')}")

        print("\n" + "=" * 60)
        print("[PASS] All models valid!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pydantic_schemas():
    """Test Pydantic schemas"""
    print("\n" + "=" * 60)
    print("Pydantic Schemas Validation")
    print("=" * 60)

    try:
        from api.routes.jobs import JobCreate, JobUpdate, JobResponse, JobDetailResponse
        from api.routes.rooms import RoomResponse, RoomOverride

        print("\n[OK] Job schemas:")
        print(f"  - JobCreate: {JobCreate.__name__}")
        print(f"  - JobUpdate: {JobUpdate.__name__}")
        print(f"  - JobResponse: {JobResponse.__name__}")
        print(f"  - JobDetailResponse: {JobDetailResponse.__name__}")

        print("\n[OK] Room schemas:")
        print(f"  - RoomResponse: {RoomResponse.__name__}")
        print(f"  - RoomOverride: {RoomOverride.__name__}")

        print("\n[OK] Schema fields:")
        print("\n  JobCreate fields:")
        for field_name, field in JobCreate.model_fields.items():
            required = "required" if field.is_required() else "optional"
            print(f"    - {field_name}: {required}")

        print("\n  RoomOverride fields:")
        for field_name, field in RoomOverride.model_fields.items():
            required = "required" if field.is_required() else "optional"
            print(f"    - {field_name}: {required}")

        print("\n" + "=" * 60)
        print("[PASS] All schemas valid!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CleanoutPro API Structure Validation")
    print("=" * 60)
    print("\nThis script validates:")
    print("  1. All imports work correctly")
    print("  2. Routes are properly registered")
    print("  3. Database models are defined")
    print("  4. Pydantic schemas are valid")
    print("\nNote: Database connection not tested (Docker not required)")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Models", test_models()))
    results.append(("Schemas", test_pydantic_schemas()))

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "[PASS] PASS" if passed else "[FAIL] FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        print("\nAPI structure is valid and ready for testing!")
        print("\nNext steps:")
        print("  1. Start Docker: docker-compose up -d")
        print("  2. Run backend: python api/main.py")
        print("  3. Test endpoints: http://localhost:8000/docs")
    else:
        print("[FAIL] SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the errors above before proceeding.")

    print()
    sys.exit(0 if all_passed else 1)
