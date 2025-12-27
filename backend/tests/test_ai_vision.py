"""
Tests for AI Vision Service
Tests the Ollama LLaVA integration and room classification
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from services.ai_vision import AIVisionService, get_ai_vision_service


class TestAIVisionService:
    """Test AI Vision Service functionality"""

    def test_init_service(self):
        """Test service initialization"""
        service = AIVisionService(ollama_url="http://localhost:11434")
        assert service.ollama_url == "http://localhost:11434"
        assert service.model == "llava:7b"

    def test_singleton_pattern(self):
        """Test that get_ai_vision_service returns singleton"""
        service1 = get_ai_vision_service()
        service2 = get_ai_vision_service()
        assert service1 is service2

    @patch('services.ai_vision.requests.post')
    def test_classify_room_success(self, mock_post, mock_image_data, mock_ai_classification):
        """Test successful room classification"""
        # Mock Ollama API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response': json.dumps(mock_ai_classification)
        }
        mock_post.return_value = mock_response

        service = AIVisionService()
        result = service.classify_room(
            image_data=mock_image_data,
            room_name="Master Bedroom",
            use_ultrathink=True
        )

        # Verify result structure
        assert result['size_class'] == 'large'
        assert result['workload_class'] == 'heavy'
        assert result['confidence'] == 0.87
        assert 'reasoning' in result
        assert 'features' in result
        assert 'processing_time' in result

        # Verify API was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert 'llava:7b' in str(call_args)

    @patch('services.ai_vision.requests.post')
    def test_classify_room_without_ultrathink(self, mock_post, mock_image_data):
        """Test classification without ultrathink mode"""
        mock_classification = {
            "size_class": "medium",
            "workload_class": "moderate",
            "confidence": 0.75,
            "reasoning": "Standard bedroom",
            "features": {}
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response': json.dumps(mock_classification)
        }
        mock_post.return_value = mock_response

        service = AIVisionService()
        result = service.classify_room(
            image_data=mock_image_data,
            use_ultrathink=False
        )

        assert result['size_class'] == 'medium'
        assert result['workload_class'] == 'moderate'

    @patch('services.ai_vision.requests.post')
    def test_classify_room_api_error(self, mock_post, mock_image_data):
        """Test handling of Ollama API errors"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_post.return_value = mock_response

        service = AIVisionService()
        result = service.classify_room(image_data=mock_image_data)

        # Should return fallback classification
        assert result['size_class'] == 'medium'
        assert result['workload_class'] == 'moderate'
        assert result['confidence'] == 0.0
        assert 'error' in result

    @patch('services.ai_vision.requests.post')
    def test_classify_room_timeout(self, mock_post, mock_image_data):
        """Test handling of timeout errors"""
        mock_post.side_effect = Exception("Timeout")

        service = AIVisionService()
        result = service.classify_room(image_data=mock_image_data)

        # Should return fallback classification
        assert result['size_class'] == 'medium'
        assert result['workload_class'] == 'moderate'
        assert result['confidence'] == 0.0

    def test_parse_classification_valid_json(self):
        """Test parsing valid JSON classification"""
        service = AIVisionService()

        valid_json = json.dumps({
            "size_class": "large",
            "workload_class": "heavy",
            "confidence": 0.87,
            "reasoning": "Test reasoning",
            "features": {"clutter_density": 0.75}
        })

        result = service._parse_classification(valid_json)
        assert result['size_class'] == 'large'
        assert result['workload_class'] == 'heavy'
        assert result['confidence'] == 0.87

    def test_parse_classification_invalid_size(self):
        """Test parsing with invalid size class"""
        service = AIVisionService()

        invalid_json = json.dumps({
            "size_class": "huge",  # Invalid
            "workload_class": "heavy",
            "confidence": 0.87
        })

        result = service._parse_classification(invalid_json)
        # Should default to 'medium'
        assert result['size_class'] == 'medium'
        assert result['workload_class'] == 'heavy'

    def test_parse_classification_invalid_workload(self):
        """Test parsing with invalid workload class"""
        service = AIVisionService()

        invalid_json = json.dumps({
            "size_class": "large",
            "workload_class": "insane",  # Invalid
            "confidence": 0.87
        })

        result = service._parse_classification(invalid_json)
        assert result['size_class'] == 'large'
        # Should default to 'moderate'
        assert result['workload_class'] == 'moderate'

    def test_parse_classification_confidence_bounds(self):
        """Test that confidence is clamped between 0 and 1"""
        service = AIVisionService()

        # Test confidence > 1
        json_high = json.dumps({
            "size_class": "large",
            "workload_class": "heavy",
            "confidence": 1.5
        })
        result = service._parse_classification(json_high)
        assert result['confidence'] == 1.0

        # Test confidence < 0
        json_low = json.dumps({
            "size_class": "large",
            "workload_class": "heavy",
            "confidence": -0.5
        })
        result = service._parse_classification(json_low)
        assert result['confidence'] == 0.0

    def test_parse_classification_malformed_json(self):
        """Test parsing completely malformed JSON"""
        service = AIVisionService()

        malformed = "This is not JSON at all"
        result = service._parse_classification(malformed)

        # Should return fallback
        assert result['size_class'] == 'medium'
        assert result['workload_class'] == 'moderate'
        assert result['confidence'] == 0.0
        assert 'parse_error' in result

    def test_parse_classification_json_in_text(self):
        """Test extracting JSON from surrounding text"""
        service = AIVisionService()

        text_with_json = """
        Here is my analysis:
        {"size_class": "large", "workload_class": "heavy", "confidence": 0.87}
        That's my assessment.
        """

        result = service._parse_classification(text_with_json)
        assert result['size_class'] == 'large'
        assert result['workload_class'] == 'heavy'

    @patch('services.ai_vision.requests.get')
    def test_connection_check_success(self, mock_get):
        """Test successful connection check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        service = AIVisionService()
        assert service.test_connection() is True

    @patch('services.ai_vision.requests.get')
    def test_connection_check_failure(self, mock_get):
        """Test failed connection check"""
        mock_get.side_effect = Exception("Connection refused")

        service = AIVisionService()
        assert service.test_connection() is False

    @patch('services.ai_vision.requests.get')
    def test_model_installed_check_success(self, mock_get):
        """Test checking if LLaVA model is installed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [
                {'name': 'llava:7b'},
                {'name': 'llama2:7b'}
            ]
        }
        mock_get.return_value = mock_response

        service = AIVisionService()
        assert service.check_model_installed() is True

    @patch('services.ai_vision.requests.get')
    def test_model_installed_check_not_found(self, mock_get):
        """Test when LLaVA model is not installed"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [
                {'name': 'llama2:7b'}
            ]
        }
        mock_get.return_value = mock_response

        service = AIVisionService()
        assert service.check_model_installed() is False

    def test_build_classification_prompt_with_ultrathink(self):
        """Test prompt building with ultrathink enabled"""
        service = AIVisionService()
        prompt = service._build_classification_prompt("Master Bedroom", use_ultrathink=True)

        assert "Master Bedroom" in prompt
        assert "ULTRATHINK MODE ENABLED" in prompt
        assert "ROOM SIZE ANALYSIS" in prompt
        assert "CONFIDENCE EVALUATION" in prompt

    def test_build_classification_prompt_without_ultrathink(self):
        """Test prompt building without ultrathink"""
        service = AIVisionService()
        prompt = service._build_classification_prompt("Kitchen", use_ultrathink=False)

        assert "Kitchen" in prompt
        assert "ULTRATHINK MODE ENABLED" not in prompt
        assert "SIZE CLASSES" in prompt
        assert "WORKLOAD CLASSES" in prompt
