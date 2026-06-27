# Nuhoot — Development Guide

## Rules for AI Agents Working on This Codebase

### MANDATORY: Test-Driven Development (TDD)

**RED → GREEN → REFACTOR. No exceptions.**

1. Write a failing test that describes the behavior you want
2. Run it. Watch it fail. (RED)
3. Write the minimum code to make it pass. (GREEN)
4. Refactor. Run tests again. (REFACTOR)
5. Commit only when all tests pass

**Never write production code without a test first.** If you're adding a feature, the test comes first. If you're fixing a bug, the test that reproduces the bug comes first.

### MANDATORY: Code Quality Gates

Before ANY commit, ALL of these must pass:

```bash
ruff check src/ tests/          # Linting — zero errors
black --check src/ tests/       # Formatting — zero diffs
mypy src/                        # Type checking — zero errors
pytest -x -q                     # Tests — all pass
```

**If any gate fails, the commit is BLOCKED.** Fix the issue, don't bypass the gate.

### MANDATORY: Commit Conventions

```
type(scope): concise description

Types: feat, fix, refactor, test, docs, chore, ci
Scopes: finder, investigator, crafter, sender, api, db, auth, config

Examples:
  feat(finder): add Google Maps scraper with category filter
  fix(sender): handle WhatsApp API rate limit (429)
  test(crafter): add tests for Arabic pitch generation
  refactor(api): extract business routes into separate module
```

### MANDATORY: Branch Strategy

- `main` — production-ready, all tests pass, deployable
- `develop` — integration branch for features
- `feature/<name>` — individual features
- `fix/<name>` — bug fixes

**Never commit directly to `main`.** Always work on a feature branch, then merge after tests pass.

### MANDATORY: File Organization

```
src/nuhoot/
├── api/routes/     # One file per resource (businesses.py, campaigns.py)
├── services/       # One file per service (finder.py, investigator.py, crafter.py, sender.py)
├── models/         # One file per domain model (business.py, campaign.py, message.py)
├── ai/             # AI client wrappers
├── whatsapp/       # WhatsApp API client
├── utils/          # Pure functions, no side effects
└── config.py       # Settings via pydantic-settings
```

**Rules:**
- Each file does ONE thing well
- No file > 300 lines. Split if it grows.
- No circular imports. Services depend on models, never the reverse.
- API routes are thin — delegate to services.
- Services contain business logic. Models are data containers.
- Utils are pure functions with no side effects.

### MANDATORY: Error Handling

- Every external API call must have try/except with specific exception types
- Never use bare `except:` — always catch specific exceptions
- Log errors with context (what failed, what inputs, what was expected)
- Return meaningful error messages to API callers, not stack traces
- Use custom exception classes for domain-specific errors

### MANDATORY: Configuration

- ALL secrets in `.env` — never hardcoded, never committed
- ALL settings via `pydantic-settings` (type-safe, validated)
- `.env.example` documents every variable — keep it in sync
- No magic numbers — use constants or config values

### MANDATORY: Database

- Use SQLAlchemy ORM for all database operations
- Migrations via Alembic — never modify schema manually
- Each model has a primary key, created_at, and updated_at
- Foreign keys have explicit `ondelete` behavior
- Indexes on frequently queried columns

### MANDATORY: API Design

- RESTful conventions: GET (list), POST (create), PUT (update), DELETE (remove)
- Pagination on all list endpoints (page, per_page params)
- Input validation via Pydantic models
- Consistent response format: `{"success": bool, "data": ..., "error": ...}`
- HTTP status codes: 200, 201, 400, 404, 422, 500

### MANDATORY: Testing Standards

- Unit tests: mock external dependencies (API calls, database)
- Integration tests: real database (test container), real HTTP calls
- E2E tests: full pipeline from API endpoint to expected outcome
- Coverage target: 80% minimum for src/
- Test names: `test_<what>_<condition>` (e.g., `test_finder_returns_businesses_for_valid_category`)
- One assertion concept per test (use multiple tests, not multiple asserts)

### MANDATORY: Docker

- Multi-stage builds (build deps, then copy to slim runtime)
- Non-root user in container
- Health check on every service
- .dockerignore excludes tests, docs, .git, __pycache__
- Pin base image versions (python:3.12-slim, not python:latest)

### MANDATORY: Security

- Input sanitization on all user inputs
- SQL injection prevention (SQLAlchemy parameterized queries)
- Rate limiting on API endpoints
- CORS configured explicitly (not `*`)
- Secrets never logged, never returned in API responses
- WhatsApp messages include PDPL opt-out text

### MANDATORY: Arabic Language Support

- All user-facing text available in Arabic and English
- RTL layout support in dashboard
- Saudi phone format: +966 5X XXX XXXX
- Date/time in Asia/Riyadh timezone
- Currency in SAR

### Build Pipeline Phases

**Phase 1: Finder** — Google Maps scraper service
**Phase 2: Investigator** — Social media + website analysis
**Phase 3: Crafter** — AI pitch generation (Arabic + English)
**Phase 4: Sender** — WhatsApp Cloud API integration
**Phase 5: Dashboard** — Web UI for campaigns and analytics

Each phase: write tests → implement → test → review → merge. No phase skips the next.
