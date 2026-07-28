from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db

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