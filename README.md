# Hotel Front Desk Shift Handover

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)

A FastAPI backend for managing front desk shift handovers — agents open a 12-hour shift (9am–9pm / 9pm–9am), log notes during the shift, and close it so the next agent can review and acknowledge outstanding items.

## Status

✅ v1 complete — all endpoints built, tested end-to-end, and committed. Frontend and deployment are next.

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

Once running, explore and test all endpoints at `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/` | Register a new user |
| POST | `/login` | Log in, returns JWT |
| POST | `/shifts/start` | Start a new shift |
| GET | `/shifts/current` | View current shift + notes |
| POST | `/shifts/close` | Close shift (requires a summary note) |
| GET | `/shifts/history` | View past shifts + notes |
| POST | `/notes/create` | Add a note |
| PATCH | `/notes/{id}/acknowledge` | Acknowledge a note |

## Business rules enforced

- Only one shift can be open at a time
- A shift can't close without a logged summary note
- Notes can't be added once a shift is closed
- A user can't acknowledge their own note