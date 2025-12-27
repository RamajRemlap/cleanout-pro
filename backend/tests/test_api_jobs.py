"""
Tests for Jobs API endpoints
Tests CRUD operations and job management
"""

import pytest
from datetime import datetime, timedelta
import uuid


class TestJobsAPI:
    """Test Jobs API endpoints"""

    def test_list_jobs_empty(self, client, test_db):
        """Test listing jobs when database is empty"""
        response = client.get("/api/jobs")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_jobs(self, client, sample_job):
        """Test listing all jobs"""
        response = client.get("/api/jobs")
        assert response.status_code == 200

        jobs = response.json()
        assert len(jobs) == 1
        assert jobs[0]['job_number'] == sample_job.job_number
        assert jobs[0]['status'] == 'draft'

    def test_list_jobs_with_status_filter(self, client, test_db, sample_customer):
        """Test filtering jobs by status"""
        from database.models import Job

        # Create jobs with different statuses
        job1 = Job(
            customer_id=sample_customer.id,
            job_number="JOB-001",
            status="draft",
            property_address="123 Main St"
        )
        job2 = Job(
            customer_id=sample_customer.id,
            job_number="JOB-002",
            status="completed",
            property_address="456 Oak Ave"
        )

        test_db.add(job1)
        test_db.add(job2)
        test_db.commit()

        # Filter by draft status
        response = client.get("/api/jobs?status=draft")
        assert response.status_code == 200
        jobs = response.json()
        assert len(jobs) == 1
        assert jobs[0]['status'] == 'draft'

        # Filter by completed status
        response = client.get("/api/jobs?status=completed")
        assert response.status_code == 200
        jobs = response.json()
        assert len(jobs) == 1
        assert jobs[0]['status'] == 'completed'

    def test_list_jobs_with_pagination(self, client, test_db, sample_customer):
        """Test job listing pagination"""
        from database.models import Job

        # Create multiple jobs
        for i in range(10):
            job = Job(
                customer_id=sample_customer.id,
                job_number=f"JOB-{i:03d}",
                status="draft",
                property_address=f"{i} Test St"
            )
            test_db.add(job)

        test_db.commit()

        # Test limit
        response = client.get("/api/jobs?limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5

        # Test offset
        response = client.get("/api/jobs?offset=5&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_create_job_success(self, client, sample_customer):
        """Test successful job creation"""
        job_data = {
            "customer_id": str(sample_customer.id),
            "property_address": "789 Elm Street, Anytown, USA",
            "notes": "Full house cleanout"
        }

        response = client.post("/api/jobs", json=job_data)
        assert response.status_code == 201

        job = response.json()
        assert job['customer_id'] == str(sample_customer.id)
        assert job['property_address'] == "789 Elm Street, Anytown, USA"
        assert job['status'] == 'draft'
        assert job['notes'] == "Full house cleanout"
        assert 'job_number' in job
        assert job['base_estimate'] == 0.0
        assert job['ai_estimate'] == 0.0

    def test_create_job_with_scheduled_date(self, client, sample_customer):
        """Test creating job with scheduled date"""
        scheduled = (datetime.now() + timedelta(days=7)).isoformat()

        job_data = {
            "customer_id": str(sample_customer.id),
            "property_address": "123 Test St",
            "scheduled_date": scheduled
        }

        response = client.post("/api/jobs", json=job_data)
        assert response.status_code == 201

        job = response.json()
        assert job['scheduled_date'] is not None

    def test_create_job_customer_not_found(self, client):
        """Test creating job with non-existent customer"""
        job_data = {
            "customer_id": str(uuid.uuid4()),
            "property_address": "123 Test St"
        }

        response = client.post("/api/jobs", json=job_data)
        assert response.status_code == 404
        assert "Customer not found" in response.json()['detail']

    def test_create_job_invalid_customer_id(self, client):
        """Test creating job with invalid UUID"""
        job_data = {
            "customer_id": "not-a-uuid",
            "property_address": "123 Test St"
        }

        response = client.post("/api/jobs", json=job_data)
        assert response.status_code == 422  # Validation error

    def test_get_job_success(self, client, sample_job):
        """Test getting job details"""
        response = client.get(f"/api/jobs/{sample_job.id}")
        assert response.status_code == 200

        job = response.json()
        assert job['id'] == str(sample_job.id)
        assert job['job_number'] == sample_job.job_number
        assert 'customer' in job
        assert 'rooms' in job

    def test_get_job_with_rooms(self, client, sample_job, sample_room):
        """Test getting job with room details"""
        response = client.get(f"/api/jobs/{sample_job.id}")
        assert response.status_code == 200

        job = response.json()
        assert len(job['rooms']) == 1
        assert job['rooms'][0]['name'] == 'Master Bedroom'
        assert job['rooms'][0]['ai_size_class'] == 'large'
        assert job['rooms'][0]['ai_workload_class'] == 'heavy'

    def test_get_job_not_found(self, client):
        """Test getting non-existent job"""
        response = client.get(f"/api/jobs/{uuid.uuid4()}")
        assert response.status_code == 404
        assert "Job not found" in response.json()['detail']

    def test_update_job_status(self, client, sample_job):
        """Test updating job status"""
        update_data = {"status": "in_progress"}

        response = client.patch(f"/api/jobs/{sample_job.id}", json=update_data)
        assert response.status_code == 200

        job = response.json()
        assert job['status'] == 'in_progress'

    def test_update_job_scheduled_date(self, client, sample_job):
        """Test updating scheduled date"""
        new_date = (datetime.now() + timedelta(days=14)).isoformat()

        update_data = {"scheduled_date": new_date}

        response = client.patch(f"/api/jobs/{sample_job.id}", json=update_data)
        assert response.status_code == 200

        job = response.json()
        assert job['scheduled_date'] is not None

    def test_update_job_human_adjusted_estimate(self, client, sample_job):
        """Test updating human adjusted estimate"""
        update_data = {"human_adjusted_estimate": 1250.00}

        response = client.patch(f"/api/jobs/{sample_job.id}", json=update_data)
        assert response.status_code == 200

        job = response.json()
        assert job['human_adjusted_estimate'] == 1250.00
        assert job['final_price'] == 1250.00  # Should update final_price

    def test_update_job_adjustments(self, client, sample_job):
        """Test updating job adjustments (stairs, bins, etc.)"""
        update_data = {
            "adjustments": [
                {"type": "stairs", "amount": 75.00, "reason": "3 flights"},
                {"type": "bin_rental", "amount": 200.00, "reason": "20 yard"}
            ]
        }

        response = client.patch(f"/api/jobs/{sample_job.id}", json=update_data)
        assert response.status_code == 200

        job = response.json()
        assert len(job['adjustments']) == 2

    def test_update_job_not_found(self, client):
        """Test updating non-existent job"""
        update_data = {"status": "completed"}

        response = client.patch(f"/api/jobs/{uuid.uuid4()}", json=update_data)
        assert response.status_code == 404

    def test_delete_job_success(self, client, sample_job):
        """Test deleting job"""
        response = client.delete(f"/api/jobs/{sample_job.id}")
        assert response.status_code == 204

        # Verify job is deleted
        response = client.get(f"/api/jobs/{sample_job.id}")
        assert response.status_code == 404

    def test_delete_job_cascades_to_rooms(self, client, sample_job, sample_room, test_db):
        """Test that deleting job also deletes rooms"""
        from database.models import Room

        # Verify room exists
        room = test_db.query(Room).filter(Room.id == sample_room.id).first()
        assert room is not None

        # Delete job
        response = client.delete(f"/api/jobs/{sample_job.id}")
        assert response.status_code == 204

        # Verify room is also deleted (cascade)
        room = test_db.query(Room).filter(Room.id == sample_room.id).first()
        assert room is None

    def test_delete_job_not_found(self, client):
        """Test deleting non-existent job"""
        response = client.delete(f"/api/jobs/{uuid.uuid4()}")
        assert response.status_code == 404

    def test_get_job_estimate_no_rooms(self, client, sample_job):
        """Test getting estimate for job with no rooms"""
        response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        assert response.status_code == 200

        estimate = response.json()
        assert estimate['ai_estimate'] == 0.0
        assert estimate['room_breakdown'] == []

    def test_get_job_estimate_with_rooms(self, client, sample_job, sample_room):
        """Test getting estimate for job with rooms"""
        response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        assert response.status_code == 200

        estimate = response.json()
        assert estimate['job_id'] == str(sample_job.id)
        assert estimate['ai_estimate'] > 0
        assert len(estimate['room_breakdown']) == 1
        assert estimate['room_breakdown'][0]['name'] == 'Master Bedroom'

    def test_get_job_estimate_with_human_adjustment(self, client, sample_job, sample_room):
        """Test estimate includes human adjustment when present"""
        # Update job with human adjustment
        client.patch(f"/api/jobs/{sample_job.id}", json={"human_adjusted_estimate": 1500.00})

        response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        assert response.status_code == 200

        estimate = response.json()
        assert estimate['human_adjusted_estimate'] == 1500.00

    def test_get_job_estimate_not_found(self, client):
        """Test getting estimate for non-existent job"""
        response = client.get(f"/api/jobs/{uuid.uuid4()}/estimate")
        assert response.status_code == 404
