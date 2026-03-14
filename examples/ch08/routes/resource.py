from fastapi import APIRouter

router = APIRouter(prefix="/generate", tags=["Resource"])

@router.get("/text")
def serve_language_model_controller():
    pass

@router.get("/audio")
def serve_text_to_audio_model_controller():
    pass