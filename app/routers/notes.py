from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, oauth2,schemas
from ..database import get_db



router = APIRouter(
    prefix="/notes",
    tags=["Note"]
)



@router.post("/create")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):

    current_shift = db.query(models.Shift).filter(models.Shift.status == "open").first()
    if not current_shift:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add a note — no shift is currently open"
        )

    new_note = models.Note(
        **note.dict(),
        shift_id=current_shift.id,
        author_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note