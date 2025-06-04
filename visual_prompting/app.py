"""FastAPI application for Visual Prompting web interface."""

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import OPENROUTER_API_KEY, validate_config
from .llm import image_to_base64, run_llm
from .schema import AspectRatio, ImagePrompt, VideoPrompt

app = FastAPI(title="Visual Prompting API", description="AI-powered structured prompt generation for visual media", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate configuration on startup
validate_config()

# Mount static files
UI_DIR = Path(__file__).parent.parent / "visual-prompting-ui"
if UI_DIR.exists():
    app.mount("/static", StaticFiles(directory=UI_DIR), name="static")


class GenerationRequest(BaseModel):
    """Request model for prompt generation."""

    mode: str  # "image" or "video"
    text_input: Optional[str] = None
    num_outputs: int = 1
    aspect_ratio: Optional[AspectRatio] = None


class GenerationResponse(BaseModel):
    """Response model for generated prompts."""

    status: str
    prompts: list[str]
    mode: str
    num_outputs: int


def success_response(message: str, data: dict = None) -> dict:
    """Standard success response format."""
    response = {"status": "success", "message": message}
    if data:
        response.update(data)
    return response


@app.get("/")
async def root():
    """Serve the simple HTML interface."""
    ui_file = UI_DIR / "simple-ui.html"
    if ui_file.exists():
        return FileResponse(ui_file)
    else:
        return {"message": "Visual Prompting API is running", "ui": "Visit /static/simple-ui.html for the interface"}


@app.post("/api/generate", response_model=GenerationResponse)
async def generate_prompts(request: GenerationRequest):
    """Generate structured prompts for image or video creation."""
    try:
        prompts = []
        user_text = request.text_input or "A beautiful scene"

        for i in range(request.num_outputs):
            # Use the run_llm function directly
            prompt_str = run_llm(user_request=user_text, media_type=request.mode, return_string=True)
            prompts.append(prompt_str)

        return GenerationResponse(status="success", prompts=prompts, mode=request.mode, num_outputs=request.num_outputs)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/api/generate-with-image")
async def generate_with_image(mode: str, num_outputs: int = 1, text_input: Optional[str] = None, image: Optional[UploadFile] = File(None)):
    """Generate prompts with optional image input."""
    try:
        prompts = []
        user_text = text_input or "A beautiful scene"
        image_path = None

        if image:
            # Read and save image temporarily
            image_content = await image.read()
            temp_path = Path(f"/tmp/{image.filename}")
            with open(temp_path, "wb") as f:
                f.write(image_content)
            image_path = str(temp_path)

        for i in range(num_outputs):
            # Use the run_llm function with image path
            prompt_str = run_llm(user_request=user_text, media_type=mode, image_path=image_path, return_string=True)
            prompts.append(prompt_str)

        # Clean up temp file
        if image_path and Path(image_path).exists():
            Path(image_path).unlink()

        return GenerationResponse(status="success", prompts=prompts, mode=mode, num_outputs=num_outputs)

    except Exception as e:
        # Clean up temp file on error
        if "image_path" in locals() and image_path and Path(image_path).exists():
            Path(image_path).unlink()
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/api/enums")
async def get_enums():
    """Get all available enum values for the UI."""
    from .schema import (
        AspectRatio,
        CameraMovement,
        LensType,
        LightingType,
        PhotographyType,
        ShotType,
    )

    return {
        "aspect_ratios": [{"value": ratio.value, "label": ratio.value} for ratio in AspectRatio],
        "shot_types": [{"value": shot.value, "label": shot.value.replace("_", " ").title()} for shot in ShotType],
        "camera_movements": [{"value": movement.value, "label": movement.value.replace("_", " ").title()} for movement in CameraMovement],
        "photography_types": [{"value": photo.value, "label": photo.value.replace("_", " ").title()} for photo in PhotographyType],
        "lens_types": [{"value": lens.value, "label": lens.value.replace("_", " ").title()} for lens in LensType],
        "lighting_types": [{"value": light.value, "label": light.value.replace("_", " ").title()} for light in LightingType],
    }


def main():
    """Run the FastAPI application."""
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    host = os.getenv("HOST", "localhost")

    print(f"🎨 Visual Prompting Studio starting...")
    print(f"🌐 Web interface: http://{host}:{port}")
    print(f"📖 API docs: http://{host}:{port}/docs")

    uvicorn.run("visual_prompting.app:app", host=host, port=port, reload=True, log_level="info")


if __name__ == "__main__":
    main()
