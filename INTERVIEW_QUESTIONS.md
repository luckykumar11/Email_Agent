# INTERVIEW_QUESTIONS.md

## Email Agent — Interview Questions & Answers

### Python

**Q: How does async/await work in Python?**
A: Python's async/await enables cooperative multitasking. `async def` defines a coroutine, `await` pauses execution until the awaited coroutine completes, allowing the event loop to run other tasks. In FastAPI, this enables handling many concurrent requests without threads.

**Q: What is the purpose of `__slots__` in Python classes?**
A: `__slots__` restricts instance attributes to a defined set, reducing memory usage and improving attribute access speed. Useful for ORM models with many instances.

**Q: Explain context managers in Python.**
A: Context managers use `__enter__`/`__exit__` (or `@contextmanager` decorator) to manage resources. Used for database sessions, file handling, and SMTP connections — ensuring cleanup even on errors.

### FastAPI

**Q: How does FastAPI dependency injection work?**
A: `Depends()` declares dependencies that FastAPI resolves automatically. For example, `get_current_user` depends on `get_db`, which depends on the database engine. Dependencies can be overridden for testing.

**Q: Why use FastAPI over Flask/Django?**
A: Native async support, automatic OpenAPI docs, Pydantic validation, dependency injection, and performance comparable to Go/Node.js. For this project, async was essential for database and SMTP operations.

**Q: How does FastAPI handle request validation?**
A: Pydantic models validate request bodies, query parameters, and path parameters automatically. Invalid requests return 422 errors with detailed field-level messages.

### Pydantic

**Q: What changed in Pydantic v2?**
A: Core rewritten in Rust for 5-50x performance. `field_validator` replaces `@validator`. `model_config` replaces `class Config`. `model_dump()` replaces `.dict()`. TypedDict and other improvements.

**Q: How does Pydantic prevent SQL injection?**
A: Pydantic validates and sanitizes input at the API boundary. SQLAlchemy's ORM uses parameterized queries, preventing SQL injection. Combined, user input never reaches raw SQL.

### SQLAlchemy

**Q: What is the N+1 query problem and how did you solve it?**
A: Loading a company and then accessing each related service triggers separate queries. Solved with `selectinload` in the repository layer to eagerly load relationships in a single query.

**Q: Explain SQLAlchemy session lifecycle.**
A: Session tracks pending changes. `commit()` flushes to DB. `expire_on_commit=False` keeps objects usable after commit. Async sessions use `async_sessionmaker` for non-blocking operations.

**Q: Why use repository pattern?**
A: Separates data access from business logic. Makes testing easier (mock repositories), keeps services focused on logic, and provides a consistent interface for database operations.

### PostgreSQL

**Q: What indexes did you create and why?**
A: `ix_users_email` for fast login lookups. `ix_email_history_company_id` for filtering history by company. Unique constraints on company_id for email_config, signature, and preferences prevent duplicates.

**Q: How do you handle database migrations?**
A: Alembic generates and tracks migrations. Each migration is a versioned Python script. `alembic upgrade head` applies pending migrations. Production never uses `create_all()`.

### Alembic

**Q: Why use Alembic instead of `create_all()`?**
A: `create_all()` can't handle schema changes (adding columns, modifying types). Alembic tracks migration history, supports upgrades/downgrades, and works safely in production with multiple environments.

### REST API

**Q: How do you handle pagination?**
A: Email history uses offset/limit pagination with `page` and `page_size` query parameters. Response includes total count for UI pagination controls.

**Q: What HTTP status codes do you use and why?**
A: 201 for creation, 204 for deletion, 400 for bad requests, 401 for unauthorized, 404 for not found, 409 for conflicts, 422 for validation errors, 500 for server errors.

### JWT Authentication

**Q: How does JWT work in this project?**
A: On login, server creates a token with user ID and expiry, signed with SECRET_KEY. Client sends token in Authorization header. `get_current_user` dependency decodes and validates it.

**Q: What are JWT limitations?**
A: Can't be revoked (until expiry). No server-side session store. Mitigated by short expiry (30 min default). Production could add token blacklist or use refresh tokens.

**Q: Why JWT over session cookies?**
A: Stateless (no server storage), works across domains, mobile-friendly, scales horizontally. Trade-off: can't revoke immediately.

### SMTP & Email Security

**Q: What is the difference between STARTTLS and SSL/TLS?**
A: STARTTLS upgrades a plain connection to encrypted (port 587). SSL/TLS connects encrypted from the start (port 465). Both provide encryption; STARTTLS is more common for submission.

**Q: How are SMTP passwords protected?**
A: Encrypted with bcrypt before storage. Never returned in API responses. The API returns `password_configured: true/false` instead.

**Q: Why not use a global SMTP account?**
A: Each company sends through their own configured SMTP. This ensures proper sender identity, deliverability, and compliance. The system never hardcodes email credentials.

### AI / LLM

**Q: How do you prevent prompt injection?**
A: System prompt instructs the LLM that company data is reference-only, not to follow embedded instructions, not to invent facts, and to only return structured JSON.

**Q: Why use a provider abstraction for LLM?**
A: Decouples application from specific API. MockLLMProvider enables testing without API keys. Easy to add new providers. Application remains functional even if external LLM is unavailable.

**Q: How do you handle LLM hallucination?**
A: System prompt explicitly forbids inventing facts. Company context is provided as structured reference data. Generated emails are always reviewed by the user before sending.

### Next.js

**Q: Why use App Router over Pages Router?**
A: App Router supports React Server Components, layouts, nested routes, and streaming. Better code organization with co-located components and server/client component splitting.

**Q: How does client-side auth work?**
A: JWT stored in localStorage. AuthContext provides token/user to all pages. API client attaches token to requests. 401 responses trigger automatic redirect to login.

**Q: How is the API client structured?**
A: Centralized `lib/api.ts` with typed methods for each endpoint. Handles auth headers, error parsing, and 401 redirect. Environment variable for base URL.

### Testing

**Q: How do you test without real SMTP?**
A: Mock SMTP with `unittest.mock.patch`. Tests verify the correct SMTP methods are called with correct arguments. `MockLLMProvider` for AI tests.

**Q: How do you test data isolation?**
A: Create two users, each with their own company and config. Verify User A's API calls only return User A's data, never User B's.

**Q: What testing frameworks are used?**
A: pytest + pytest-asyncio for async tests. httpx AsyncClient for API testing. unittest.mock for SMTP and LLM mocking. SQLite + aiosqlite for test database.

### Docker

**Q: Why use Docker Compose?**
A: Orchestrates PostgreSQL, backend, and frontend services. Consistent development environment. `docker-compose up --build` starts everything with one command.

**Q: How is networking configured?**
A: Services communicate via service names (db, backend). Frontend calls backend via localhost:3000 -> localhost:8000 in dev, or via Docker network in production.

### Architecture

**Q: Why separate repositories from services?**
A: Single Responsibility. Repositories handle data access, services handle business logic. Easier to test, modify, and understand. Follows clean architecture principles.

**Q: How would you scale this to production?**
A: Add Redis for caching, Celery for email queue, load balancer, monitoring (Prometheus/Grafana), structured logging, rate limiting, and proper secrets management (Vault/AWS Secrets Manager).
