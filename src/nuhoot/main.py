"""FastAPI application entry point."""

from fastapi import FastAPI

from nuhoot.api.routes.businesses import router as businesses_router

app = FastAPI(
    title="Nuhoot",
    description="AI-powered lead generation for Saudi marketing agencies",
    version="0.1.0",
)

app.include_router(businesses_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "nuhoot"}
