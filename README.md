# Hotel Front Desk Shift Handover

A FastAPI backend for managing front desk shift handovers — agents open a 12-hour shift (9am–9pm / 9pm–9am), log notes during the shift, and close it so the next agent can review and acknowledge outstanding items.

## Status
🚧 In development (v1: manual shift start/close, single-role front desk staff)

## Stack
- FastAPI
- PostgreSQL + SQLAlchemy
- JWT auth (OAuth2 password flow)

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # then fill in your values
uvicorn app.main:app --reload
```
