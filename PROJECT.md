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
| type | str | `general` or `summary` — default `general` |
| content | text | free text either way — summary notes contain the structured room/cash/sales block as plain text, not separate validated fields |
| acknowledged | bool | default false |
| acknowledged_by | FK → Users.id, nullable | |
| acknowledged_at | timestamp, nullable | |
| created_at | timestamp | |

**Safeguard rule:** an agent cannot open a new shift if one is already `open`.

**New safeguard rule:** a shift cannot be closed unless at least one `summary`-type note exists for it. The system does not validate the contents of the summary (room counts, cash figures) — only that one was logged before closing.

**New safeguard rule:** once a shift is `closed`, no new notes (of any type) can be added to it. Notes can only be created against the currently `open` shift.

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
│   ├── main.py                 ✅ done (registration only wired in)
│   ├── database.py             ✅ done
│   ├── config.py               ✅ done
│   ├── models.py                ✅ done (Users, Shift, Note)
│   ├── schemas.py                ✅ UserCreate/UserOut done; UserLogin/Token unused leftovers
│   ├── utils.py                   ✅ done (password hashing)
│   ├── oauth2.py                   ✅ done (JWT create/verify, wired in)
│   └── routers/
│       ├── __init__.py
│       ├── auth.py                 ✅ done (login)
│       ├── users.py                 ✅ done (register)
│       ├── shifts.py                  ✅ done (start shift)
│       └── notes.py                    ⬜ not started
```

## 7. Build Strategy: Piece by Piece

Instead of writing all routers at once, we build **one small piece at a time** and fully test each in `/docs` before moving to the next. This isolates bugs immediately instead of stacking them across files.

| # | Piece | Status |
|---|---|---|
| 1 | Register user (`POST /users/`) | ✅ **Done, tested, committed** |
| 2 | Login (`POST /login`, returns JWT) | ✅ **Done, tested, committed** |
| 3 | Start shift (`POST /shifts/start`) | ✅ **Done, tested, committed** |
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
| Frontend direction | Decided on FastAPI + Jinja2 templates (server-rendered HTML) over a separate React app, since no prior frontend experience — mockups created for login page, dashboard, and shift history view. Frontend work sequenced *after* all 8 backend pieces are complete. |
| Design change | Notes now have a `type` field: `general` (default, anything) or `summary` (structured shift-end report — room status, cash float, sales, as free text). A shift **cannot be closed** unless at least one `summary` note exists for it — enforced in the close-shift route, not via field-level validation of the summary's contents. |
| Process change | Switched to a guided/hands-on build style: concept explained first, user writes or reasons through code, diagnoses errors from tracebacks before being told the fix. Applied starting with piece #2. |
| **Piece #2 complete** | Created `routers/auth.py`, added `TokenData` back to `schemas.py`, wired `auth.router` into `main.py`. Fixed missing `python-multipart` dependency (required by `OAuth2PasswordRequestForm`). Tested in `/docs`: correct login returns JWT token; wrong password/email both return `403 Forbidden` with the same generic message. |
| **Piece #2 committed** | Login endpoint committed and pushed to GitHub |
| Bug fixed | `TokenData.id` was typed as `str`, but `user.id` is an `int` (matches the `Integer` column in `models.py`) — caused a Pydantic validation error the first time an authenticated route (`start_shift`) actually decoded a real token. Fixed by changing `TokenData.id` to `int`, since forcing a numeric DB id through the token as a string served no purpose. |
| Piece #3 in progress | Writing `routers/shifts.py` — `start_shift` endpoint: blocks if a shift is already open, otherwise creates a new `Shift` row with `opened_by=current_user.id`. Wired into `main.py`. Discovered the `TokenData` bug above while testing this via `/docs` (first real use of `Depends(oauth2.get_current_user)`). |
| **Piece #3 complete** | Tested via `/docs`: (1) happy path — starting a shift with none open succeeds, returns correct `opened_by`/`start_time`/`status`; (2) safeguard — attempting to start a second shift while one is open correctly fails with "A shift is already open." Both the success case and the failure/safeguard case were verified, not just the happy path. |
| **Piece #3 committed** | Start shift endpoint committed and pushed to GitHub |

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

## 10. Functional Requirements (FR)

**User Management**
- FR1: Register with email + password
- FR2: Reject registration if email already in use
- FR3: Hash passwords before storing; never return plaintext or hash in responses
- FR4: Login with email + password, receive JWT access token
- FR5: Reject invalid login with a generic error (don't reveal which field was wrong)

**Shift Management**
- FR6: Authenticated user can start a new shift
- FR7: Prevent starting a new shift if one is already open
- FR8: Record who opened a shift and when
- FR9: Authenticated user can close an open shift
- FR10: Record who closed a shift and when
- FR11: Any authenticated user can view the current open shift, including its notes
- FR12: Any authenticated user can view history of past closed shifts
- FR13: Derive Day/Night label from start_time hour (not stored separately)

**Note (Handover) Management**
- FR14: Authenticated user can add a text note to the currently open shift, tagged as either `general` or `summary` type
- FR14a: Notes default to `general` type if none specified
- FR15: Record who authored a note and when
- FR16: Authenticated user can mark a note as acknowledged
- FR17: Record who acknowledged a note and when
- FR18: Notes display embedded within their parent shift (current or historical), visually distinguishing summary notes from general notes
- FR19: A shift cannot be closed unless at least one `summary`-type note exists for it; attempting to close without one returns a clear error and blocks the action

## 11. Non-Functional Requirements (NFR)

**Security**
- NFR1: Passwords hashed with bcrypt; never logged or persisted in plaintext
- NFR2: Secrets/credentials live in environment variables, never hardcoded
- NFR3: All shift/note-modifying endpoints require a valid JWT (401 if missing/invalid)
- NFR4: Ownership fields (author, opened_by, acknowledged_by) always derived server-side, never accepted as client input

**Reliability / Data Integrity**
- NFR5: Only one shift can be open at any given time (app-level enforcement)
- NFR6: FK constraints ensure notes/shifts can't exist without valid parents
- NFR7: Deleting a user doesn't cascade-delete their shifts/notes — only nulls the reference

**Maintainability**
- NFR8: Clear separation: models (data) / schemas (API contracts) / routers (endpoints) / utils (hashing, auth)
- NFR9: All configuration centralized in one settings module
- NFR10: Built and tested incrementally — one endpoint at a time, verified in `/docs` before the next

**Usability**
- NFR11: API responses never expose password hashes, regardless of endpoint
- NFR12: Clear, specific error messages without leaking raw system/database errors

**Performance / Scalability (v1 scope)**
- NFR13: Designed for a single hotel property, small number of concurrent staff — not multi-tenant
- NFR14: Use SQLAlchemy relationships for shift/note queries, avoiding N+1 patterns where reasonable

## 12. Build Plan & Timeline

**Approach:** one piece at a time, fully tested in `/docs` before moving to the next. Each row below gets checked off only when tested AND committed to git — not just written.

| # | Piece | Covers | Est. time | Status |
|---|---|---|---|---|
| 1 | Register user | FR1–FR3, NFR1, NFR11 | 30–45 min | ✅ Done & committed |
| 2 | Login | FR4–FR5, NFR2–NFR3 | 30–45 min | ✅ Done & committed |
| 3 | Start shift | FR6–FR8, NFR5 | 45–60 min | ✅ Done & committed |
| 4 | Get current shift | FR11, FR13 | 20–30 min | ⬜ Not started |
| 5 | Create note | FR14–FR15, FR14a, NFR4 | 30–45 min | ⬜ Not started |
| 6 | Close shift | FR9–FR10, FR19 (summary required) | 30–45 min | ⬜ Not started |
| 7 | Shift history | FR12, FR18 | 30–45 min | ⬜ Not started |
| 8 | Acknowledge note | FR16–FR17 | 20–30 min | ⬜ Not started |

**Total estimated remaining time:** ~3.5–5.5 hours of active build time (spread across however many sessions fit your schedule — hotel shifts + MBA coursework come first).

**Pacing options:**
- *Steady pace:* 1 piece per session → backend complete in 4–7 sessions, whenever they happen
- *Focused push:* 2 pieces/day → backend complete in ~3–4 days, only if you have dedicated blocks

**After all 8 pieces are done (v1 backend complete):**

| Phase | What | Est. time |
|---|---|---|
| Full flow test | Walk the entire journey once: register → login → start shift → add notes → close → view history → acknowledge | 1 session |
| Polish | Add `GET /users/me`, tidy error messages, review NFR checklist above | 1 session |
| **Decision point** | Frontend (simple HTML/JS or React) vs. API-only portfolio vs. deploy (Render/Railway) — decide once backend is solid, not before | — |

**Rule going forward:** don't check a row off in this table until it's (1) tested successfully in `/docs`, and (2) committed to git. If a session ends mid-piece, leave it marked ⏸️ Paused with a note in Section 8 (Progress Log) on exactly where it stopped — same as we did for login.