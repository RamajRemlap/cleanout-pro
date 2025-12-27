"""
Jobs API Routes
CRUD operations for job management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid

from database.connection import get_db
from database.models import Job, Customer, Room
from pydantic import BaseModel

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


# Pydantic schemas for request/response
class JobCreate(BaseModel):
    customer_id: str
    property_address: str
    scheduled_date: Optional[datetime] = None
    notes: Optional[str] = None


class JobUpdate(BaseModel):
    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    human_adjusted_estimate: Optional[float] = None
    adjustments: Optional[List[dict]] = None
    notes: Optional[str] = None


class JobResponse(BaseModel):
    id: str
    customer_id: str
    job_number: str
    status: str
    property_address: str
    scheduled_date: Optional[datetime]
    completed_date: Optional[datetime]
    base_estimate: float
    ai_estimate: float
    human_adjusted_estimate: float
    final_price: float
    adjustments: List[dict]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobDetailResponse(JobResponse):
    customer: dict
    rooms: List[dict]

    class Config:
        from_attributes = True


# Routes

@router.get("", response_model=List[JobResponse])
def list_jobs(
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List all jobs with optional filtering

    Query params:
    - status: Filter by status (draft, estimated, approved, in_progress, completed, invoiced, paid)
    - limit: Max results (default 50, max 100)
    - offset: Pagination offset
    """
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(limit).all()

    return jobs


@router.post("", response_model=JobResponse, status_code=201)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create new job

    Requires:
    - customer_id: UUID of existing customer
    - property_address: Job location
    """
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == uuid.UUID(job_data.customer_id)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Generate job number (simple: JOB-timestamp)
    job_number = f"JOB-{int(datetime.now().timestamp())}"

    # Create job
    job = Job(
        customer_id=uuid.UUID(job_data.customer_id),
        job_number=job_number,
        property_address=job_data.property_address,
        scheduled_date=job_data.scheduled_date,
        notes=job_data.notes,
        status='draft'
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/{job_id}", response_model=JobDetailResponse)
def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Get job details with customer and rooms

    Returns complete job information including:
    - Customer details
    - All rooms with AI classification
    - Pricing breakdown
    """
    job = db.query(Job).options(
        joinedload(Job.customer),
        joinedload(Job.rooms)
    ).filter(Job.id == uuid.UUID(job_id)).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Format response
    response = {
        **JobResponse.from_orm(job).dict(),
        "customer": {
            "id": str(job.customer.id),
            "name": job.customer.name,
            "email": job.customer.email,
            "phone": job.customer.phone,
            "address": job.customer.address
        },
        "rooms": [
            {
                "id": str(room.id),
                "name": room.name,
                "room_number": room.room_number,
                "image_url": room.image_url,
                "ai_size_class": room.ai_size_class,
                "ai_workload_class": room.ai_workload_class,
                "ai_confidence": room.ai_confidence,
                "human_size_class": room.human_size_class,
                "human_workload_class": room.human_workload_class,
                "final_size_class": room.final_size_class,
                "final_workload_class": room.final_workload_class,
                "estimated_cost": float(room.estimated_cost) if room.estimated_cost else 0.0,
                "created_at": room.created_at
            }
            for room in job.rooms
        ]
    }

    return response


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: str,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    """
    Update job

    Can update:
    - status
    - scheduled_date, completed_date
    - human_adjusted_estimate (override AI estimate)
    - adjustments (stairs, bins, etc.)
    - notes
    """
    job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update fields
    update_data = job_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(job, field):
            setattr(job, field, value)

    # Recalculate final_price if estimates changed
    if job_update.human_adjusted_estimate is not None:
        job.final_price = Decimal(str(job_update.human_adjusted_estimate))

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete job (cascade deletes rooms)

    WARNING: This permanently deletes the job and all associated rooms
    """
    job = db.query(Job).filter(Job.id == uuid.UUID(job_id)).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return None


@router.get("/{job_id}/estimate", response_model=dict)
def get_job_estimate(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Get pricing estimate for job

    Returns:
    - AI estimate (sum of all room AI estimates)
    - Human adjusted estimate (if set)
    - Final price
    - Breakdown by room
    """
    job = db.query(Job).options(joinedload(Job.rooms)).filter(Job.id == uuid.UUID(job_id)).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Calculate AI estimate from rooms
    ai_total = sum(float(room.estimated_cost) for room in job.rooms)

    room_breakdown = [
        {
            "room_id": str(room.id),
            "name": room.name,
            "size_class": room.final_size_class,
            "workload_class": room.final_workload_class,
            "cost": float(room.estimated_cost)
        }
        for room in job.rooms
    ]

    return {
        "job_id": str(job.id),
        "ai_estimate": ai_total,
        "human_adjusted_estimate": float(job.human_adjusted_estimate) if job.human_adjusted_estimate else None,
        "adjustments": job.adjustments or [],
        "final_price": float(job.final_price) if job.final_price else ai_total,
        "room_breakdown": room_breakdown
    }
