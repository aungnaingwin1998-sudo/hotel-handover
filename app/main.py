from fastapi import FastAPI
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Front Desk Shift Handover")


@app.get("/")
def root():
    return {"message": "Hotel Handover API is running"}