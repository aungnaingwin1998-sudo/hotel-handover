from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"]
)

@router.post("/start")
def start_shift(db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):

    existing_open_shift = db.query(models.Shift).filter(models.Shift.status == "open").first()
    if existing_open_shift:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A shift is already open"
        )

    new_shift = models.Shift(opened_by=current_user.id)
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)

    return new_shift

@router.get("/current")
def get_current_shift (db: Session = Depends(get_db),current_user: models.Users = Depends(oauth2.get_current_user)):
    current_shift=db.query(models.Shift).filter(models.Shift.status=='open').first()
    if  not current_shift:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="There is not shift opened yet")
    return current_shift

@router.post("/close")
def close_shift(db: Session = Depends(get_db),current_user: models.Users = Depends(oauth2.get_current_user)):
    current_shift=db.query(models.Shift).filter(models.Shift.status=='open').first()
    if not current_shift:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="There is not shift opened yet")

    note_check=db.query(models.Note).filter(models.Note.shift_id==current_shift.id, models.Note.type=="summary").first()
    if not note_check:
        raise HTTPException(status_code=400, detail="Cannot close shift — no summary note has been logged")
    current_shift.status = "closed"
    current_shift.end_time = datetime.now()
    current_shift.closed_by = current_user.id
    db.commit()
    db.refresh(current_shift)
    return current_shift
