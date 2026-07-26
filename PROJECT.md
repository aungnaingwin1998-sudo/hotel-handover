# Hotel Front Desk Shift Handover — Project Proposal & Progress

## 1. Overview

A backend web app for hotel front desk staff to hand over information between shifts. Built as a portfolio project, informed by real front desk experience at Chilli Salza Patong Beach Hotel, Phuket.

**Problem it solves:** Front desk shifts run 12 hours (9am–9pm / 9pm–9am). Information about guest requests, issues, and follow-ups currently has no structured system to pass from one shift to the next. This app gives agents a simple, reliable way to log notes during a shift and ensures the next agent sees them.

## 2. Scope (v1)

- Single role: all users are front desk staff (no housekeeping/manager roles yet)
- Manual shift lifecycle: agent clicks "Start Shift" and "Close Shift" — no auto-scheduling
- Notes are plain text (no category/priority — that's v2)
- Notes can be acknowledged by the next agent, tracked with who + when
- Full shift history browsable (not just the latest shift)
- Shift type (Day/Night) is **derived** from `start_time` hour, not stored as its own field

## 3. Explicitly Out of Scope (v2+ ideas)

- Roles beyond front desk (housekeeping, maintenance, manager)
- Note categories/priority tags (guest issue, VIP, maintenance, urgent, etc.)
- Task assignment system (follow-ups assigned to a specific person, tracked done/not done)
- Automatic shift open/close based on system time (cron/scheduler)
- Frontend UI (this phase is backend/API only)

## 4. Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL, accessed via SQLAlchemy ORM
- **Auth:** JWT (OAuth2 password flow), bcrypt password hashing
- **Config:** pydantic-settings reading from `.env` (no hardcoded secrets)
- **Dev tools:** venv, pgAdmin for DB inspection

## 5. Data Model

**Users**
| field | type | notes |
|---|---|---|
| id | int, PK | |
| email | str, unique | |
| password | str | bcrypt hash |
| created_at | timestamp | |

**Shift**
| field | type | notes |
|---|---|---|
| id | int, PK | |
| start_time | timestamp | set when opened |
| end_time | timestamp, nullable | set when closed |
| status | str | `open` / `closed` |
| opened_by | FK → Users.id | |
| closed_by | FK → Users.id, nullable | |

Day/Night label is derived from `start_time` hour at query/display time — not a stored column.

**Note**
| field | type | notes |
|---|---|---|
| id | int, PK | |
| shift_id | FK → Shift.id | |
| author_id | FK → Users.id | |
| content | text | |
| acknowledged | bool | default false |
| acknowledged_by | FK → Users.id, nullable | |
| acknowledged_at | timestamp, nullable | |
| created_at | timestamp | |

**Safeguard rule:** an agent cannot open a new shift if one is already `open`.

## 6. File Structure

```
hotel-handover/
├── .env                      # real secrets — gitignored
├── .env.example              # template, committed
├── .gitignore
├── README.md
├── PROJECT.md                # this file
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py                ✅ done (minimal version, routers not yet wired in)
│   ├── database.py            ✅ done
│   ├── config.py              ✅ done
│   ├── models.py               ✅ done (Users, Shift, Note)
│   ├── schemas.py               ⬜ not started
│   ├── utils.py                  ⬜ not started (password hashing)
│   ├── oauth2.py                  ⬜ not started (JWT create/verify)
│   └── routers/
│       ├── __init__.py
│       ├── auth.py                ⬜ not started (/login)
│       ├── users.py                ⬜ not started (register, get me)
│       ├── shifts.py                ⬜ not started (start, close, current, history)
│       └── notes.py                  ⬜ not started (create, acknowledge)
```

## 7. Build Strategy: Piece by Piece

Instead of writing all routers at once, we build **one small piece at a time** and fully test each in `/docs` before moving to the next. This isolates bugs immediately instead of stacking them across files.

| # | Piece | Status |
|---|---|---|
| 1 | Register user (`POST /users/`) | ✅ **Done, tested, committed** |
| 2 | Login (`POST /login`, returns JWT) | ⏸️ **Paused** — some groundwork exists but not finished or tested (see note below) |
| 3 | Start shift (`POST /shifts/start`) | ⬜ Not started |
| 4 | Get current shift (`GET /shifts/current`) | ⬜ Not started |
| 5 | Create note (`POST /shifts/{id}/notes`) | ⬜ Not started |
| 6 | Close shift (`POST /shifts/{id}/close`) | ⬜ Not started |
| 7 | Shift history (`GET /shifts/history`) | ⬜ Not started |
| 8 | Acknowledge note (`PATCH /notes/{id}/acknowledge`) | ⬜ Not started |

**Important:** `schemas.py` only contains schemas for pieces already built (currently just `UserCreate`/`UserOut`, plus unused leftovers `UserLogin`/`Token` from the paused login attempt). Schemas for shifts and notes get added exactly when we build that piece — not before. Same philosophy for `main.py`'s `include_router()` calls — **`main.py` currently only includes `users.router`**, nothing else.

**Note on paused login work:** `oauth2.py` has a full JWT create/verify implementation already written (reads `SECRET_KEY` from `.env` via `settings`, not hardcoded). `routers/auth.py` was never actually created as a file, so login is **not wired into `main.py` and cannot be tested yet**. This is safe — the unused code in `oauth2.py`/`schemas.py` doesn't affect the working app. Pick this up whenever ready by creating `routers/auth.py` (draft already given in chat history) and adding `auth.router` to `main.py`.

## 8. Progress Log

| Date/step | What happened |
|---|---|
| Design | Discussed flow-first: shift lifecycle, note lifecycle, acknowledgment, history browsing |
| Decision | 12-hour fixed shifts (9–9), manual start/close (not auto-scheduled) |
| Decision | Track who acknowledges each note + when (not just true/false) |
| Decision | Build piece by piece, test each in `/docs` before moving on |
| models.py | Written and committed — Users, Shift, Note with proper FK relationships |
| Repo | Git initialized, pushed to GitHub, cloned locally to `OneDrive/Desktop/hotel-handover` |
| config.py | Written — pydantic Settings loading from `.env` |
| database.py | Written — SQLAlchemy engine, SessionLocal, Base, get_db() dependency |
| Debugging | Fixed: `.env` missing → created it; fixed empty `SECRET_KEY`; fixed wrong Postgres password; **created `hotel_handover` database manually in pgAdmin** (SQLAlchemy only creates tables, not the database itself) |
| Debugging | Fixed missing packages (`fastapi`, `sqlalchemy`, `psycopg2-binary`, `python-jose`, `passlib`, `bcrypt`, `python-dotenv`, `pydantic-settings`, `email-validator`) not installed in venv |
| Debugging | Fixed `bcrypt` 5.x incompatibility with `passlib` — downgraded to `bcrypt==4.0.1` |
| Debugging | Fixed repeated corruption of `main.py` (stray import line from `routers/users.py` accidentally pasted in) |
| Debugging | Fixed typos in `routers/users.py`: `utils.hashed` → `utils.hash`, `user.dict` → `user.dict()`, missing `()` on `db.commit`/`db.refresh` |
| **Piece #1 complete** | `POST /users/` tested via `/docs` — returns `201 Created`, password stored as bcrypt hash, confirmed in pgAdmin |
| **Piece #1 committed** | Registration-only version committed and pushed to GitHub |
| Login attempt | Started piece #2 — wrote `oauth2.py` JWT logic and draft `routers/auth.py`, but paused before creating/testing the auth router file. Decision made to keep `main.py` clean (registration only) and commit that as a stable checkpoint before resuming login. |

## 9. Next Steps (pick up here)

**Resume Piece #2: Login** (whenever ready)

1. Create `app/routers/auth.py` (draft content already exists — see chat history or ask to regenerate it)
2. Add `auth.router` to `main.py`:
   ```python
   from .routers import users, auth
   ...
   app.include_router(auth.router)
   ```
3. Test in `/docs`: log in with the test user from piece #1, confirm a JWT token comes back (`access_token`, `token_type: "bearer"`)
4. Commit: `"Piece 2: login endpoint (JWT), tested via /docs"`
5. Once confirmed working → move to Piece #3 (Start shift)
