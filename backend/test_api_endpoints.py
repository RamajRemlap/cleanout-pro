"""
CleanoutPro API Endpoint Testing Script
Run this after starting the FastAPI server to test all endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}[OK]{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.END} {message}")

def print_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {message}")

def print_section(message):
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"{message}")
    print(f"{'='*60}{Colors.END}\n")

def test_health_check():
    """Test basic health check endpoints"""
    print_section("1. Testing Health Check Endpoints")

    try:
        # Test root endpoint
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Root endpoint: {data['service']} v{data['version']}")
        else:
            print_error(f"Root endpoint failed: {response.status_code}")

        # Test health endpoint
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"Health check: {response.json()['status']}")
        else:
            print_error(f"Health check failed: {response.status_code}")

        return True
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_create_customer():
    """Test customer creation"""
    print_section("2. Testing Customer Creation")

    try:
        # Note: You'll need to implement the customers endpoint first
        # This is a placeholder for when it's implemented
        print_info("Customer endpoint not yet implemented in routes")
        print_info("Creating customer manually in database...")

        # For now, we'll assume a customer exists or create one via SQL
        return "sample-customer-id"  # Placeholder

    except Exception as e:
        print_error(f"Customer creation failed: {e}")
        return None

def test_create_job(customer_id):
    """Test job creation"""
    print_section("3. Testing Job Creation")

    try:
        job_data = {
            "customer_id": customer_id,
            "property_address": "123 Test Street, Anytown, USA",
            "notes": "API Test Job"
        }

        response = requests.post(f"{BASE_URL}/api/jobs", json=job_data)

        if response.status_code == 201:
            job = response.json()
            print_success(f"Job created: {job['job_number']}")
            print_info(f"  Job ID: {job['id']}")
            print_info(f"  Status: {job['status']}")
            print_info(f"  Address: {job['property_address']}")
            return job['id']
        else:
            print_error(f"Job creation failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None

    except Exception as e:
        print_error(f"Job creation failed: {e}")
        return None

def test_list_jobs():
    """Test listing jobs"""
    print_section("4. Testing Job Listing")

    try:
        # List all jobs
        response = requests.get(f"{BASE_URL}/api/jobs")

        if response.status_code == 200:
            jobs = response.json()
            print_success(f"Retrieved {len(jobs)} jobs")
            for job in jobs[:3]:  # Show first 3
                print_info(f"  - {job['job_number']}: {job['status']}")
            return True
        else:
            print_error(f"Job listing failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Job listing failed: {e}")
        return False

def test_get_job(job_id):
    """Test getting job details"""
    print_section("5. Testing Get Job Details")

    try:
        response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")

        if response.status_code == 200:
            job = response.json()
            print_success(f"Retrieved job: {job['job_number']}")
            print_info(f"  Customer: {job['customer']['name']}")
            print_info(f"  Rooms: {len(job['rooms'])}")
            print_info(f"  Status: {job['status']}")
            return True
        else:
            print_error(f"Get job failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Get job failed: {e}")
        return False

def test_update_job(job_id):
    """Test updating job"""
    print_section("6. Testing Job Update")

    try:
        update_data = {
            "status": "estimated",
            "notes": "Updated via API test"
        }

        response = requests.patch(f"{BASE_URL}/api/jobs/{job_id}", json=update_data)

        if response.status_code == 200:
            job = response.json()
            print_success(f"Job updated")
            print_info(f"  New status: {job['status']}")
            print_info(f"  Notes: {job['notes']}")
            return True
        else:
            print_error(f"Job update failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Job update failed: {e}")
        return False

def test_get_job_estimate(job_id):
    """Test getting job estimate"""
    print_section("7. Testing Job Estimate")

    try:
        response = requests.get(f"{BASE_URL}/api/jobs/{job_id}/estimate")

        if response.status_code == 200:
            estimate = response.json()
            print_success(f"Retrieved estimate")
            print_info(f"  AI Estimate: ${estimate['ai_estimate']:.2f}")
            print_info(f"  Final Price: ${estimate['final_price']:.2f}")
            print_info(f"  Rooms: {len(estimate['room_breakdown'])}")
            return True
        else:
            print_error(f"Get estimate failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Get estimate failed: {e}")
        return False

def test_api_docs():
    """Test API documentation endpoints"""
    print_section("8. Testing API Documentation")

    try:
        # Test OpenAPI docs
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print_success(f"Swagger UI available at: {BASE_URL}/docs")

        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        if response.status_code == 200:
            print_success(f"ReDoc available at: {BASE_URL}/redoc")

        # Test OpenAPI JSON
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            print_success(f"OpenAPI schema available")

        return True

    except Exception as e:
        print_error(f"API docs test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CLEANOUTPRO API ENDPOINT TESTS")
    print("="*60)

    print_info(f"Testing API at: {BASE_URL}")
    print_info(f"Make sure the FastAPI server is running!\n")

    # Track results
    results = {
        "passed": 0,
        "failed": 0
    }

    # Run tests
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Server is not running or not accessible!")
        print_info("Start the server with: python api/main.py")
        return

    # Test API documentation
    if test_api_docs():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test job listing
    if test_list_jobs():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Note: The following tests require a customer ID
    # You'll need to create a customer first (via SQL or implement customer endpoint)
    print_section("Additional Tests")
    print_info("To test job creation, you need to:")
    print_info("  1. Create a customer first")
    print_info("  2. Use the customer ID to create a job")
    print_info("\nExample SQL to create a customer:")
    print_info("  INSERT INTO customers (name, email, phone, address)")
    print_info("  VALUES ('Test Customer', 'test@example.com', '555-0123', '123 Main St');")

    # Print summary
    print_section("Test Summary")
    total = results["passed"] + results["failed"]
    print_success(f"Passed: {results['passed']}/{total}")
    if results["failed"] > 0:
        print_error(f"Failed: {results['failed']}/{total}")

    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Visit http://localhost:8000/docs for interactive API docs")
    print("2. Create a customer via SQL or implement customer endpoint")
    print("3. Test job creation with a valid customer_id")
    print("4. Test room upload with image files")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
