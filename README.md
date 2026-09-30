# Email Agent — Profile & Email Configuration Module

A full-stack application for managing company profiles, email configurations, and AI-powered email generation/sending.

## Problem Statement

Build a production-quality Email Agent that allows companies to register, configure their SMTP accounts, and use AI to generate professional emails using their company context — with complete multi-user data isolation.

## Features

- **Authentication**: JWT-based registration and login
- **Company Profile**: Full CRUD with services, target customers, value propositions, social links
- **Email Configuration**: SMTP setup with encrypted password storage
- **SMTP Testing**: Verify configuration before sending
- **Email Signature**: Create, manage, and auto-append signatures
- **Email Preferences**: Customize sender, reply-to, CC/BCC defaults, format
- **AI Email Agent**: Generate emails using company context via LLM provider abstraction
- **Email Sending**: Send through company's configured SMTP account
- **Email History**: Track all sent emails with pagination
- **Data Isolation**: Multi-user/multi-company — each user only accesses their own data

## Architecture

```
Frontend (Next.js)  ──>  Backend (FastAPI)  ──>  Database (PostgreSQL)
                              │
                              ├── AI Provider (Gemini / Mock)
                              └── SMTP Service (Company-configured)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, SQLAlchemy 2.x, Pydantic v2, Alembic |
| Database | PostgreSQL (SQLite for development) |
| Auth | JWT (python-jose), bcrypt password hashing |
| AI | Google Gemini / Mock LLM Provider |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Testing | pytest, httpx, unittest.mock |
| Infrastructure | Docker, Docker Compose |

## Project Structure

```
email-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── core/                # Config, security, dependencies
│   │   ├── db/                  # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── repositories/        # Data access layer
│   │   ├── services/            # Business logic
│   │   ├── providers/llm/       # AI provider abstraction
│   │   └── api/v1/              # API routes
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Test suite (50 tests)
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Next.js pages
│   ├── components/              # React components
│   ├── lib/                     # API client, types, auth
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Database Tables

| Table | Description |
|-------|------------|
| users | User accounts with hashed passwords |
| companies | Company profiles linked to users |
| services_products | Company offerings |
| target_customers | Customer segments |
| value_propositions | Value statements |
| social_links | Social media links |
| email_configurations | SMTP settings (encrypted passwords) |
| email_signatures | Email signatures |
| email_preferences | Sending preferences |
| email_history | Sent email records |

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` — Register new user
- `POST /api/v1/auth/login` — Login and receive JWT
- `GET /api/v1/auth/me` — Get current user

### Company
- `POST /api/v1/company` — Create company profile
- `GET /api/v1/company` — Get company profile
- `PUT /api/v1/company` — Update company profile

### Email Configuration
- `POST /api/v1/email-config` — Create SMTP config
- `GET /api/v1/email-config` — Get SMTP config (password not returned)
- `PUT /api/v1/email-config` — Update SMTP config
- `POST /api/v1/email-config/test` — Test SMTP connection

### Signature
- `POST /api/v1/signature` — Create signature
- `GET /api/v1/signature` — Get signature
- `PUT /api/v1/signature` — Update signature
- `DELETE /api/v1/signature` — Delete signature

### Preferences
- `POST /api/v1/preferences` — Create preferences
- `GET /api/v1/preferences` — Get preferences
- `PUT /api/v1/preferences` — Update preferences

### Email Agent
- `POST /api/v1/agent/generate-email` — Generate email with AI

### Emails
- `POST /api/v1/emails/send` — Send email
- `GET /api/v1/emails/history` — Get email history (paginated)

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
uvicorn app.main:app --reload
```

Swagger docs available at: http://localhost:8000/docs

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local if needed
npm run dev
```

Frontend available at: http://localhost:3000

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./email_agent.db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
LLM_PROVIDER=mock          # "mock" or "gemini"
LLM_API_KEY=               # Required only for gemini
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## LLM Configuration

Set `LLM_PROVIDER=mock` to use the built-in mock provider (no API key needed).
Set `LLM_PROVIDER=gemini` and provide `LLM_API_KEY` to use Google Gemini.

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

## Docker

```bash
docker-compose up --build
```

This starts PostgreSQL, backend (port 8000), and frontend (port 3000).

## Security

- Passwords hashed with bcrypt
- SMTP passwords encrypted and never returned in API responses
- JWT-based authentication with configurable expiry
- Multi-user data isolation enforced at repository level
- CORS restricted to configured origins
- No secrets committed to repository
- Prompt injection protection in AI system prompt
