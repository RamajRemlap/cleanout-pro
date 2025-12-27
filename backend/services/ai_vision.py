"""
AI Vision Service
Ollama LLaVA integration with "Ultrathink" extended reasoning
Classifies room images for size and workload estimation
"""

import base64
import requests
import json
import time
import re
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AIVisionService:
    """
    AI Vision service using Ollama LLaVA for room classification

    Implements "Ultrathink" - extended chain-of-thought reasoning
    for more accurate room size and workload classification
    """

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llava:7b"  # LLaVA 7B model

    def classify_room(
        self,
        image_data: bytes,
        room_name: str = "",
        use_ultrathink: bool = True
    ) -> Dict:
        """
        Classify room from image using LLaVA vision model

        Args:
            image_data: Raw image bytes (JPEG/PNG)
            room_name: Name of room (optional, helps context)
            use_ultrathink: Enable extended reasoning (recommended)

        Returns:
            {
                "size_class": "large",
                "workload_class": "heavy",
                "confidence": 0.85,
                "reasoning": "Ultrathink chain-of-thought...",
                "features": {
                    "clutter_density": 0.75,
                    "accessibility": "difficult",
                    "stairs_required": false,
                    "hazmat_present": false,
                    "salvage_potential": "medium",
                    "item_categories": ["furniture", "boxes"]
                },
                "processing_time": 12.5
            }
        """
        start_time = time.time()

        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # Construct prompt
            prompt = self._build_classification_prompt(room_name, use_ultrathink)

            # Call Ollama API
            logger.info(f"Classifying room: {room_name or 'unnamed'} (ultrathink={use_ultrathink})")

            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower for consistent classification
                    "num_predict": 1000 if use_ultrathink else 500
                }
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120  # Vision models can be slow
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.text}")

            result = response.json()
            llm_output = result.get('response', '')

            # Parse LLM output
            classification = self._parse_classification(llm_output)

            processing_time = time.time() - start_time
            classification['processing_time'] = round(processing_time, 2)

            logger.info(
                f"Classification complete: {classification['size_class']}/{classification['workload_class']} "
                f"(confidence: {classification['confidence']:.2f}, time: {processing_time:.2f}s)"
            )

            return classification

        except Exception as e:
            logger.error(f"AI vision error: {e}", exc_info=True)
            processing_time = time.time() - start_time

            # Return fallback classification with error
            return {
                'size_class': 'medium',
                'workload_class': 'moderate',
                'confidence': 0.0,
                'reasoning': f'AI classification failed: {str(e)}',
                'features': {},
                'processing_time': round(processing_time, 2),
                'error': str(e)
            }

    def _build_classification_prompt(self, room_name: str, use_ultrathink: bool) -> str:
        """Build prompt for room classification"""

        context = f"\n\nRoom being analyzed: {room_name}" if room_name else ""

        base_prompt = f"""You are analyzing a room photo for a junk removal/cleanout business.{context}

Your task: Classify the room SIZE and WORKLOAD difficulty.

SIZE CLASSES:
- small: Closet, bathroom, small bedroom (< 100 sq ft)
- medium: Standard bedroom, office (100-200 sq ft)
- large: Master bedroom, large office, garage (200-400 sq ft)
- extra_large: Basement, attic, commercial space (> 400 sq ft)

WORKLOAD CLASSES:
- light: Minimal items, easy access, mostly empty boxes/bags
- moderate: Standard clutter, some furniture, normal access
- heavy: Significant clutter, large furniture, difficult access, many items
- extreme: Hoarding situation, structural obstacles, hazmat, very dense packing

FEATURES TO IDENTIFY:
- clutter_density: 0.0 (empty) to 1.0 (packed full)
- accessibility: "easy", "moderate", "difficult"
- stairs_required: true/false (if visible)
- hazmat_present: true/false (chemicals, mold, etc.)
- salvage_potential: "none", "low", "medium", "high"
- item_categories: List categories (furniture, boxes, appliances, etc.)
"""

        if use_ultrathink:
            ultrathink_addition = """
ULTRATHINK MODE ENABLED:
Before making your final classification, think through your reasoning step-by-step:

1. ROOM SIZE ANALYSIS:
   - What are the approximate dimensions based on visible walls/ceiling?
   - Can you see floor-to-ceiling height?
   - Compare furniture size to room scale

2. FLOOR SPACE OCCUPATION:
   - What percentage of floor is visible vs covered?
   - How densely are items packed?
   - Are items stacked or spread out?

3. ITEM IDENTIFICATION:
   - What types of items do you see?
   - Approximate count of major items
   - Weight/bulk assessment

4. ACCESS & MOBILITY:
   - How easy would it be to move through the room?
   - Are there clear pathways?
   - Door/hallway accessibility
   - Any obstacles (stairs, narrow spaces)?

5. COMPLICATING FACTORS:
   - Heavy items that need special equipment?
   - Fragile or hazardous materials?
   - Structural issues?

6. SALVAGE ASSESSMENT:
   - Any items that appear valuable/reusable?
   - Donation potential?

7. CONFIDENCE EVALUATION:
   - What can you see clearly?
   - What is obscured or uncertain?
   - Overall confidence in your assessment (0.0 to 1.0)

Then provide your final classification with reasoning.
"""
            base_prompt += ultrathink_addition

        output_format = """
OUTPUT FORMAT - Respond with ONLY valid JSON, no additional text:

{
  "size_class": "large",
  "workload_class": "heavy",
  "confidence": 0.87,
  "reasoning": "Your step-by-step thinking here (be detailed if Ultrathink enabled)...",
  "features": {
    "clutter_density": 0.75,
    "accessibility": "difficult",
    "stairs_required": false,
    "hazmat_present": false,
    "salvage_potential": "medium",
    "item_categories": ["furniture", "boxes", "appliances"]
  }
}

CRITICAL: Respond ONLY with the JSON object. Do not include any text before or after the JSON.
"""

        return base_prompt + output_format

    def _parse_classification(self, llm_output: str) -> Dict:
        """Parse LLM output into structured classification"""
        try:
            # Try to parse as JSON directly
            classification = json.loads(llm_output.strip())

            # Validate required fields
            required_fields = ['size_class', 'workload_class', 'confidence']
            for field in required_fields:
                if field not in classification:
                    raise ValueError(f"Missing required field: {field}")

            # Validate size_class
            valid_sizes = ['small', 'medium', 'large', 'extra_large']
            if classification['size_class'] not in valid_sizes:
                logger.warning(f"Invalid size_class: {classification['size_class']}, defaulting to 'medium'")
                classification['size_class'] = 'medium'

            # Validate workload_class
            valid_workloads = ['light', 'moderate', 'heavy', 'extreme']
            if classification['workload_class'] not in valid_workloads:
                logger.warning(f"Invalid workload_class: {classification['workload_class']}, defaulting to 'moderate'")
                classification['workload_class'] = 'moderate'

            # Ensure confidence is float between 0 and 1
            classification['confidence'] = max(0.0, min(1.0, float(classification['confidence'])))

            # Set defaults for optional fields
            if 'reasoning' not in classification:
                classification['reasoning'] = 'No reasoning provided'

            if 'features' not in classification:
                classification['features'] = {}

            return classification

        except json.JSONDecodeError:
            # Fallback: Try to extract JSON from text
            logger.warning("Failed to parse JSON directly, attempting extraction...")

            # Look for JSON object in the text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', llm_output, re.DOTALL)

            if json_match:
                try:
                    return self._parse_classification(json_match.group(0))
                except:
                    pass

            # Ultimate fallback: Return conservative estimate
            logger.error(f"Could not parse AI response: {llm_output[:200]}...")
            return {
                'size_class': 'medium',
                'workload_class': 'moderate',
                'confidence': 0.0,
                'reasoning': 'Failed to parse AI response. Using default classification.',
                'features': {},
                'parse_error': llm_output[:500]
            }

    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_model_installed(self) -> bool:
        """Check if LLaVA model is installed"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in model.get('name', '') for model in models)
            return False
        except:
            return False


# Singleton instance
_ai_vision_service = None

def get_ai_vision_service(ollama_url: str = "http://localhost:11434") -> AIVisionService:
    """Get AI vision service singleton"""
    global _ai_vision_service
    if _ai_vision_service is None:
        _ai_vision_service = AIVisionService(ollama_url)
    return _ai_vision_service
