# SkillProof

**Verified skills and project-based hiring.** SkillProof replaces self-reported resumes with
evidence: practical assessments, isolated automated evaluation, and skill records that show their
supporting evidence.

> **Status:** Phase 2 — Authentication and Role-Based Access. Registration with email
> verification, JWT login with rotating refresh tokens, password recovery, RBAC primitives, the
> security audit log, and protected frontend routes are delivered. Assessments and evaluation
> arrive in Phases 4–5 (see [`docs/phases.md`](docs/phases.md)).

## Stack

| Area | Technology |
|---|---|
| Frontend | Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS 4, TanStack Query, Zustand |
| Backend | Django 5.2 LTS, Django REST Framework, SimpleJWT |
| Data | PostgreSQL 16, Redis 7 |
| Async | Celery worker + beat |
| Execution | Isolated Docker workers (Phase 5) |

## Repository layout

```text
SkillProof/
├── backend/           Django project (config/ + apps/ domain modules + common/)
├── frontend/          Next.js application (src/app, src/components, src/lib)
├── infrastructure/    Container definitions for API, web, and evaluation worker
├── scripts/           Developer helper scripts
└── docs/              PRD, TAD, FIS, FTL, SACS, phases, build plan
```

## Local setup

### 1. Configuration

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

The defaults target the Docker Compose services. For a database-free local run, point
`backend/.env` at SQLite:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

### 2. Run with Docker Compose

```powershell
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000/api/v1/ |
| Health | http://localhost:8000/api/v1/health/ |
| Readiness | http://localhost:8000/api/v1/health/ready/ |

### 3. Run without Docker

Backend:

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

Celery (second terminal, same environment):

```powershell
cd backend
celery -A config worker -l info --pool=solo
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

### 4. Verify the queue

With Redis, the worker, and the API running:

```powershell
cd backend
python scripts/celery_ping.py
```

The script enqueues `common.tasks.ping` and waits for the worker's result. This is the Phase 1
smoke test that proves API → Redis → Celery communication.

## Authentication (Phase 2)

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/auth/register/` | Create an account (student, employer, or university) and send a verification link |
| `POST /api/v1/auth/verify-email/` | Consume a single-use verification token |
| `POST /api/v1/auth/resend-verification/` | Reissue the verification link (authenticated) |
| `POST /api/v1/auth/login/` | Exchange credentials for an access token + refresh cookie |
| `POST /api/v1/auth/token/refresh/` | Rotate the refresh token and mint a new access token |
| `POST /api/v1/auth/logout/` | Revoke the presented refresh token |
| `GET/PATCH /api/v1/auth/me/` | Current account (writes require a verified email) |
| `POST /api/v1/auth/password-reset/` | Request a reset link (never reveals whether the email exists) |
| `POST /api/v1/auth/password-reset/confirm/` | Consume a reset token, set a new password, sign out all sessions |

Access tokens live in JavaScript memory only; the refresh token is an HttpOnly cookie that is
rotated on every use and blacklisted on logout or password reset. Privileged roles
(`administrator`) can never be self-assigned. In development, verification and reset links are
printed to the API console by the email backend.

Frontend auth surfaces: `/login`, `/register`, `/forgot-password`, `/reset-password`,
`/verify-email`, and role dashboards under `/dashboard/{student,employer,university,admin}`.
Route protection is optimistic (`src/proxy.ts` + `AuthGate`); the API remains the security
boundary.

## Quality gates

```powershell
# Backend
cd backend
ruff check .
pytest

# Frontend
cd frontend
npm run lint
npm run typecheck
npm test
npm run build
```

## Documentation

| Document | Contents |
|---|---|
| [`docs/prd.md`](docs/prd.md) | Product requirements, personas, functional requirements |
| [`docs/tad.md`](docs/tad.md) | Technical architecture, data model, scoring model, deployment |
| [`docs/fis.md`](docs/fis.md) | Frontend structure, routes, API integration |
| [`docs/ftl.md`](docs/ftl.md) | Backlog: epics and 44 feature tickets |
| [`docs/sacs.md`](docs/sacs.md) | Security, RBAC, tenant isolation, sandbox rules |
| [`docs/phases.md`](docs/phases.md) | Delivery phases, gates, sprint mapping |
| [`docs/build-plan.md`](docs/build-plan.md) | Phase-by-phase build instructions and definition of done |
