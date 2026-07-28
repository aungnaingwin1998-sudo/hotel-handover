from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users,auth,shifts

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Front Desk Shift Handover")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(shifts.router)


@app.get("/")
def root():
    return {"message": "Hotel Handover API is running"}