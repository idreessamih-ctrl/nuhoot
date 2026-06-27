"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Nuhoot",
    description="AI-powered lead generation for Saudi marketing agencies",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "nuhoot"}
