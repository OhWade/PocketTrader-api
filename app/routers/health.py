from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Returns API status and version."""
    return {"status": "ok", "version": "0.1.0"}
