# Nuhoot (نُهوت)

> AI-powered lead generation for Saudi marketing agencies.

Nuhoot finds local businesses on Google Maps, investigates their digital presence, and crafts personalized WhatsApp pitches with sample social media posts — all powered by AI.

## What It Does

1. **Find** — Scrapes Google Maps for businesses by category and location (Saudi Arabia)
2. **Investigate** — Analyzes each business's website, Instagram, SEO, and online presence
3. **Craft** — AI generates a personalized WhatsApp pitch + sample posts in Arabic
4. **Send** — Sends pitches via official WhatsApp Cloud API
5. **Track** — Dashboard showing campaign performance, response rates, and conversions

## Tech Stack

| Component | Technology | License |
|-----------|-----------|---------|
| Backend | Python 3.12 + FastAPI | MIT |
| Database | PostgreSQL 16 | PostgreSQL License |
| Queue | Redis 7 + RQ | BSD |
| Maps Scraper | gosom (Go binary) | MIT |
| AI Engine | GLM 5.2 via umans.ai | Proprietary |
| WhatsApp | Meta Cloud API | Meta ToS |
| Deploy | Docker Compose | Apache 2.0 |

## Quick Start

```bash
# Clone
git clone https://github.com/idreessamih-ctrl/nuhoot.git
cd nuhoot

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
make install

# Run database migrations
make migrate

# Start all services
make up

# Run tests
make test
```

## Development

```bash
make lint        # Run ruff + black + mypy
make test        # Run pytest
make test-cov    # Run tests with coverage
make format      # Auto-format code
make ci          # Run full CI pipeline locally
```

## Project Structure

```
nuhoot/
├── src/nuhoot/          # Application source code
│   ├── api/             # FastAPI routes
│   ├── services/        # Business logic (finder, investigator, crafter, sender)
│   ├── models/          # Database models
│   ├── ai/              # GLM 5.2 integration
│   ├── whatsapp/        # WhatsApp Cloud API client
│   └── utils/           # Shared utilities
├── tests/               # Test suite (unit, integration, e2e)
├── docker/              # Dockerfiles
├── alembic/             # Database migrations
└── docs/                # Documentation
```

## License

MIT
