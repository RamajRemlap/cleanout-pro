"""
Tests for Rooms API endpoints
Tests image upload, AI classification, and human overrides
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import uuid
import io


class TestRoomsAPI:
    """Test Rooms API endpoints"""

    def test_list_rooms_empty(self, client, test_db):
        """Test listing rooms when database is empty"""
        response = client.get("/api/rooms")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_rooms(self, client, sample_room):
        """Test listing all rooms"""
        response = client.get("/api/rooms")
        assert response.status_code == 200

        rooms = response.json()
        assert len(rooms) == 1
        assert rooms[0]['name'] == 'Master Bedroom'
        assert rooms[0]['ai_size_class'] == 'large'

    def test_list_rooms_filtered_by_job(self, client, test_db, sample_job, sample_customer):
        """Test filtering rooms by job_id"""
        from database.models import Room, Job

        # Create another job with rooms
        job2 = Job(
            customer_id=sample_customer.id,
            job_number="JOB-002",
            status="draft",
            property_address="456 Test St"
        )
        test_db.add(job2)
        test_db.commit()

        # Add rooms to both jobs
        room1 = Room(
            job_id=sample_job.id,
            name="Room 1",
            room_number=1,
            final_size_class="medium",
            final_workload_class="moderate"
        )
        room2 = Room(
            job_id=job2.id,
            name="Room 2",
            room_number=1,
            final_size_class="large",
            final_workload_class="heavy"
        )

        test_db.add(room1)
        test_db.add(room2)
        test_db.commit()

        # Filter by first job
        response = client.get(f"/api/rooms?job_id={sample_job.id}")
        assert response.status_code == 200

        rooms = response.json()
        assert len(rooms) == 1
        assert rooms[0]['job_id'] == str(sample_job.id)

    @patch('services.ai_vision.get_ai_vision_service')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_upload_room_success(
        self,
        mock_makedirs,
        mock_file_open,
        mock_ai_service,
        client,
        sample_job,
        mock_image_data,
        mock_ai_classification
    ):
        """Test successful room upload with AI classification"""
        # Mock AI service
        mock_service = MagicMock()
        mock_service.classify_room.return_value = mock_ai_classification
        mock_ai_service.return_value = mock_service

        # Create file upload
        files = {
            'image': ('test_room.jpg', io.BytesIO(mock_image_data), 'image/jpeg')
        }
        data = {
            'job_id': str(sample_job.id),
            'room_name': 'Living Room',
            'room_number': '1'
        }

        response = client.post("/api/rooms", files=files, data=data)
        assert response.status_code == 201

        room = response.json()
        assert room['name'] == 'Living Room'
        assert room['room_number'] == 1
        assert room['ai_size_class'] == 'large'
        assert room['ai_workload_class'] == 'heavy'
        assert room['ai_confidence'] == 0.87
        assert room['final_size_class'] == 'large'
        assert room['final_workload_class'] == 'heavy'
        assert room['estimated_cost'] > 0

        # Verify AI service was called
        mock_service.classify_room.assert_called_once()

    @patch('services.ai_vision.get_ai_vision_service')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_upload_room_ai_failure_fallback(
        self,
        mock_makedirs,
        mock_file_open,
        mock_ai_service,
        client,
        sample_job,
        mock_image_data
    ):
        """Test that room upload falls back to defaults when AI fails"""
        # Mock AI service failure
        mock_service = MagicMock()
        mock_service.classify_room.side_effect = Exception("AI service error")
        mock_ai_service.return_value = mock_service

        files = {
            'image': ('test_room.jpg', io.BytesIO(mock_image_data), 'image/jpeg')
        }
        data = {
            'job_id': str(sample_job.id),
            'room_name': 'Bedroom',
            'room_number': '2'
        }

        response = client.post("/api/rooms", files=files, data=data)
        assert response.status_code == 201

        room = response.json()
        # Should use fallback values
        assert room['ai_size_class'] == 'medium'
        assert room['ai_workload_class'] == 'moderate'
        assert room['ai_confidence'] == 0.0

    def test_upload_room_job_not_found(self, client, mock_image_data):
        """Test uploading room to non-existent job"""
        files = {
            'image': ('test_room.jpg', io.BytesIO(mock_image_data), 'image/jpeg')
        }
        data = {
            'job_id': str(uuid.uuid4()),
            'room_name': 'Test Room',
            'room_number': '1'
        }

        response = client.post("/api/rooms", files=files, data=data)
        assert response.status_code == 404
        assert "Job not found" in response.json()['detail']

    def test_get_room_success(self, client, sample_room):
        """Test getting room details"""
        response = client.get(f"/api/rooms/{sample_room.id}")
        assert response.status_code == 200

        room = response.json()
        assert room['id'] == str(sample_room.id)
        assert room['name'] == 'Master Bedroom'
        assert room['ai_size_class'] == 'large'
        assert room['ai_workload_class'] == 'heavy'
        assert room['ai_confidence'] == 0.87
        assert 'ai_features' in room

    def test_get_room_not_found(self, client):
        """Test getting non-existent room"""
        response = client.get(f"/api/rooms/{uuid.uuid4()}")
        assert response.status_code == 404
        assert "Room not found" in response.json()['detail']

    def test_override_room_size_only(self, client, sample_room, test_db):
        """Test human override of room size class only"""
        override_data = {
            "human_size_class": "extra_large",
            "human_override_reason": "Measured dimensions, actually larger than AI estimated"
        }

        response = client.patch(f"/api/rooms/{sample_room.id}", json=override_data)
        assert response.status_code == 200

        room = response.json()
        # AI classification preserved
        assert room['ai_size_class'] == 'large'
        assert room['ai_workload_class'] == 'heavy'

        # Human override applied
        assert room['human_size_class'] == 'extra_large'
        assert room['human_override_reason'] == "Measured dimensions, actually larger than AI estimated"

        # Final uses human override
        assert room['final_size_class'] == 'extra_large'
        assert room['final_workload_class'] == 'heavy'  # Still using AI for workload

        # Cost should be recalculated
        assert room['estimated_cost'] > 468.00  # Extra large should cost more than large

    def test_override_room_workload_only(self, client, sample_room):
        """Test human override of workload class only"""
        override_data = {
            "human_workload_class": "extreme",
            "human_override_reason": "Found hoarding situation not visible in photo"
        }

        response = client.patch(f"/api/rooms/{sample_room.id}", json=override_data)
        assert response.status_code == 200

        room = response.json()
        # AI preserved
        assert room['ai_size_class'] == 'large'
        assert room['ai_workload_class'] == 'heavy'

        # Human override applied
        assert room['human_workload_class'] == 'extreme'
        assert room['final_size_class'] == 'large'  # Still using AI
        assert room['final_workload_class'] == 'extreme'  # Using human override

    def test_override_room_both_classes(self, client, sample_room):
        """Test human override of both size and workload"""
        override_data = {
            "human_size_class": "medium",
            "human_workload_class": "light",
            "human_override_reason": "Photo misleading, room mostly empty"
        }

        response = client.patch(f"/api/rooms/{sample_room.id}", json=override_data)
        assert response.status_code == 200

        room = response.json()
        # AI preserved
        assert room['ai_size_class'] == 'large'
        assert room['ai_workload_class'] == 'heavy'

        # Human override applied
        assert room['final_size_class'] == 'medium'
        assert room['final_workload_class'] == 'light'

        # Cost should be much lower (medium/light vs large/heavy)
        assert room['estimated_cost'] < 468.00

    def test_override_updates_job_final_price(self, client, sample_job, sample_room, test_db):
        """Test that room override updates job final_price"""
        # Get initial job estimate
        initial_response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        initial_price = initial_response.json()['final_price']

        # Override room to be smaller/lighter (cheaper)
        override_data = {
            "human_size_class": "small",
            "human_workload_class": "light"
        }

        client.patch(f"/api/rooms/{sample_room.id}", json=override_data)

        # Check job estimate updated
        updated_response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        updated_price = updated_response.json()['final_price']

        assert updated_price < initial_price

    def test_override_room_not_found(self, client):
        """Test overriding non-existent room"""
        override_data = {
            "human_size_class": "large"
        }

        response = client.patch(f"/api/rooms/{uuid.uuid4()}", json=override_data)
        assert response.status_code == 404

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_room_success(self, mock_remove, mock_exists, client, sample_room):
        """Test deleting room"""
        mock_exists.return_value = True

        response = client.delete(f"/api/rooms/{sample_room.id}")
        assert response.status_code == 204

        # Verify room deleted
        response = client.get(f"/api/rooms/{sample_room.id}")
        assert response.status_code == 404

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_room_updates_job_estimate(
        self,
        mock_remove,
        mock_exists,
        client,
        test_db,
        sample_job,
        sample_room
    ):
        """Test that deleting room updates job estimate"""
        from database.models import Room

        # Add another room
        room2 = Room(
            job_id=sample_job.id,
            name="Second Room",
            room_number=2,
            final_size_class="medium",
            final_workload_class="moderate",
            estimated_cost=292.50
        )
        test_db.add(room2)
        test_db.commit()

        # Get initial job total
        initial_response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        initial_total = initial_response.json()['ai_estimate']
        assert initial_total > 0

        # Delete first room
        mock_exists.return_value = True
        client.delete(f"/api/rooms/{sample_room.id}")

        # Verify job estimate decreased
        updated_response = client.get(f"/api/jobs/{sample_job.id}/estimate")
        updated_total = updated_response.json()['ai_estimate']

        assert updated_total < initial_total
        assert updated_total == 292.50  # Only second room remains

    def test_delete_room_not_found(self, client):
        """Test deleting non-existent room"""
        response = client.delete(f"/api/rooms/{uuid.uuid4()}")
        assert response.status_code == 404

    @patch('services.ai_vision.get_ai_vision_service')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_reprocess_room_success(
        self,
        mock_file,
        mock_exists,
        mock_ai_service,
        client,
        sample_room,
        mock_ai_classification
    ):
        """Test reprocessing room with AI"""
        mock_exists.return_value = True

        # Mock AI service with new classification
        new_classification = mock_ai_classification.copy()
        new_classification['size_class'] = 'extra_large'
        new_classification['confidence'] = 0.92

        mock_service = MagicMock()
        mock_service.classify_room.return_value = new_classification
        mock_ai_service.return_value = mock_service

        response = client.post(f"/api/rooms/{sample_room.id}/reprocess")
        assert response.status_code == 200

        room = response.json()
        # AI classification updated
        assert room['ai_size_class'] == 'extra_large'
        assert room['ai_confidence'] == 0.92

        # Final also updated (since no human override)
        assert room['final_size_class'] == 'extra_large'

    @patch('services.ai_vision.get_ai_vision_service')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_reprocess_room_preserves_human_override(
        self,
        mock_file,
        mock_exists,
        mock_ai_service,
        client,
        sample_room,
        mock_ai_classification,
        test_db
    ):
        """Test that reprocessing doesn't override human judgment"""
        mock_exists.return_value = True

        # First, set human override
        sample_room.human_size_class = 'medium'
        sample_room.final_size_class = 'medium'
        test_db.commit()

        # Mock AI service
        mock_service = MagicMock()
        mock_service.classify_room.return_value = mock_ai_classification
        mock_ai_service.return_value = mock_service

        response = client.post(f"/api/rooms/{sample_room.id}/reprocess")
        assert response.status_code == 200

        room = response.json()
        # AI updated
        assert room['ai_size_class'] == 'large'

        # Human override preserved
        assert room['final_size_class'] == 'medium'  # Still human override, not AI

    @patch('os.path.exists')
    def test_reprocess_room_image_not_found(self, mock_exists, client, sample_room):
        """Test reprocessing when image file doesn't exist"""
        mock_exists.return_value = False

        response = client.post(f"/api/rooms/{sample_room.id}/reprocess")
        assert response.status_code == 400
        assert "image not found" in response.json()['detail'].lower()

    def test_reprocess_room_not_found(self, client):
        """Test reprocessing non-existent room"""
        response = client.post(f"/api/rooms/{uuid.uuid4()}/reprocess")
        assert response.status_code == 404
