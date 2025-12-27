"""
Rooms API Routes
Image upload, AI classification, and human overrides
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid
import os

from database.connection import get_db
from database.models import Room, Job
from pydantic import BaseModel
from services.ai_vision import get_ai_vision_service
from services.pricing_engine import PricingEngine


router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


# Pydantic schemas for request/response
class RoomResponse(BaseModel):
    id: str
    job_id: str
    name: str
    room_number: int
    image_url: Optional[str]

    # AI Classification
    ai_size_class: Optional[str]
    ai_workload_class: Optional[str]
    ai_confidence: Optional[float]
    ai_reasoning: Optional[str]
    ai_features: Optional[dict]

    # Human Overrides
    human_size_class: Optional[str]
    human_workload_class: Optional[str]
    human_override_reason: Optional[str]

    # Final Classification
    final_size_class: str
    final_workload_class: str

    # Pricing
    estimated_cost: float

    captured_at: datetime
    processed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoomOverride(BaseModel):
    human_size_class: Optional[str] = None
    human_workload_class: Optional[str] = None
    human_override_reason: Optional[str] = None


# Routes

@router.post("", response_model=RoomResponse, status_code=201)
async def upload_room(
    job_id: str = Form(...),
    room_name: str = Form(...),
    room_number: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload room image and trigger AI classification

    Process:
    1. Verify job exists
    2. Save image to uploads directory
    3. Trigger AI classification (Ollama LLaVA)
    4. Calculate pricing
    5. Store results

    Returns:
    - Complete room record with AI classification and cost estimate
    """
    # Verify job exists
    job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Read image data
    image_data = await image.read()

    # Save image to uploads directory
    uploads_dir = "uploads/rooms"
    os.makedirs(uploads_dir, exist_ok=True)

    # Generate unique filename
    file_extension = os.path.splitext(image.filename)[1] if image.filename else '.jpg'
    image_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = os.path.join(uploads_dir, image_filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    # Trigger AI classification
    ai_service = get_ai_vision_service()

    try:
        classification = ai_service.classify_room(image_data, room_name=room_name, use_ultrathink=True)
    except Exception as e:
        # If AI fails, use default classification
        print(f"AI classification failed: {e}")
        classification = {
            "size_class": "medium",
            "workload_class": "moderate",
            "confidence": 0.0,
            "reasoning": f"AI classification failed: {str(e)}. Using default values.",
            "features": {}
        }

    # Calculate pricing
    pricing_engine = PricingEngine()
    estimated_cost = pricing_engine.calculate_room_cost(
        classification['size_class'],
        classification['workload_class']
    )

    # Create room record
    room = Room(
        job_id=uuid.UUID(job_id),
        name=room_name,
        room_number=room_number,
        image_path=image_path,
        image_url=f"/uploads/rooms/{image_filename}",

        # AI Classification
        ai_size_class=classification['size_class'],
        ai_workload_class=classification['workload_class'],
        ai_confidence=classification['confidence'],
        ai_reasoning=classification.get('reasoning'),
        ai_features=classification.get('features', {}),

        # Final = AI (until human override)
        final_size_class=classification['size_class'],
        final_workload_class=classification['workload_class'],

        # Pricing
        estimated_cost=estimated_cost,

        processed_at=datetime.utcnow()
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    # Update job AI estimate
    job_rooms = db.query(Room).filter(Room.job_id == job.id).all()
    ai_total = sum(float(r.estimated_cost) for r in job_rooms)
    job.ai_estimate = Decimal(str(ai_total))

    # If no human adjustment, update final_price
    if not job.human_adjusted_estimate or job.human_adjusted_estimate == 0:
        job.final_price = job.ai_estimate

    db.commit()

    return room


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Get room details including AI classification and human overrides

    Returns:
    - Complete room record with all classifications and reasoning
    """
    room = db.query(Room).filter(Room.id == uuid.UUID(room_id)).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room


@router.get("", response_model=List[RoomResponse])
def list_rooms(
    job_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List rooms with optional job filtering

    Query params:
    - job_id: Filter by job
    - limit: Max results (default 100)
    - offset: Pagination offset
    """
    query = db.query(Room)

    if job_id:
        query = query.filter(Room.job_id == uuid.UUID(job_id))

    rooms = query.order_by(Room.room_number).offset(offset).limit(limit).all()

    return rooms


@router.patch("/{room_id}", response_model=RoomResponse)
def override_room_classification(
    room_id: str,
    override: RoomOverride,
    db: Session = Depends(get_db)
):
    """
    Human override for AI classification

    CRITICAL: Human judgment overrides AI
    - Updates final_size_class and final_workload_class
    - Recalculates pricing
    - Preserves original AI classification for audit
    - Updates job final_price

    This is the "Decide" part of "See, Decide, or Get Paid"
    """
    room = db.query(Room).filter(Room.id == uuid.UUID(room_id)).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Store human overrides
    if override.human_size_class:
        room.human_size_class = override.human_size_class
        room.final_size_class = override.human_size_class

    if override.human_workload_class:
        room.human_workload_class = override.human_workload_class
        room.final_workload_class = override.human_workload_class

    if override.human_override_reason:
        room.human_override_reason = override.human_override_reason

    # Recalculate pricing with human overrides
    pricing_engine = PricingEngine()
    room.estimated_cost = pricing_engine.calculate_room_cost(
        room.final_size_class,
        room.final_workload_class
    )

    db.commit()
    db.refresh(room)

    # Update job estimates
    job = db.query(Job).filter(Job.id == room.job_id).first()
    job_rooms = db.query(Room).filter(Room.job_id == job.id).all()

    # Recalculate AI estimate (sum of all AI classifications)
    ai_total = sum(
        float(pricing_engine.calculate_room_cost(r.ai_size_class, r.ai_workload_class))
        for r in job_rooms
    )
    job.ai_estimate = Decimal(str(ai_total))

    # Update final price (sum of all final classifications)
    final_total = sum(float(r.estimated_cost) for r in job_rooms)
    job.final_price = Decimal(str(final_total))

    db.commit()

    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete room and recalculate job estimates

    Also deletes associated image file
    """
    room = db.query(Room).filter(Room.id == uuid.UUID(room_id)).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    job_id = room.job_id

    # Delete image file
    if room.image_path and os.path.exists(room.image_path):
        try:
            os.remove(room.image_path)
        except Exception as e:
            print(f"Failed to delete image: {e}")

    # Delete room
    db.delete(room)
    db.commit()

    # Update job estimates
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job_rooms = db.query(Room).filter(Room.job_id == job.id).all()

        if job_rooms:
            ai_total = sum(float(r.estimated_cost) for r in job_rooms)
            job.ai_estimate = Decimal(str(ai_total))

            if not job.human_adjusted_estimate or job.human_adjusted_estimate == 0:
                job.final_price = job.ai_estimate
        else:
            # No rooms left
            job.ai_estimate = Decimal('0.00')
            job.final_price = Decimal('0.00')

        db.commit()

    return None


@router.post("/{room_id}/reprocess", response_model=RoomResponse)
def reprocess_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    Re-run AI classification on existing room image

    Useful when:
    - AI model improves
    - Initial classification failed
    - Want fresh analysis

    IMPORTANT: Does NOT override human adjustments
    Only updates ai_* fields
    """
    room = db.query(Room).filter(Room.id == uuid.UUID(room_id)).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if not room.image_path or not os.path.exists(room.image_path):
        raise HTTPException(status_code=400, detail="Room image not found")

    # Read image
    with open(room.image_path, 'rb') as f:
        image_data = f.read()

    # Re-run AI classification
    ai_service = get_ai_vision_service()

    try:
        classification = ai_service.classify_room(image_data, room_name=room.name, use_ultrathink=True)

        # Update AI fields only
        room.ai_size_class = classification['size_class']
        room.ai_workload_class = classification['workload_class']
        room.ai_confidence = classification['confidence']
        room.ai_reasoning = classification.get('reasoning')
        room.ai_features = classification.get('features', {})
        room.processed_at = datetime.utcnow()

        # Only update final if no human override exists
        if not room.human_size_class and not room.human_workload_class:
            room.final_size_class = classification['size_class']
            room.final_workload_class = classification['workload_class']

            # Recalculate pricing
            pricing_engine = PricingEngine()
            room.estimated_cost = pricing_engine.calculate_room_cost(
                room.final_size_class,
                room.final_workload_class
            )

        db.commit()
        db.refresh(room)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI classification failed: {str(e)}")

    return room
