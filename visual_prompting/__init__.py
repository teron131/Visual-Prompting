"""Visual Prompting - AI-powered structured prompt generation for visual media.

A comprehensive Python package for generating structured prompts for image and video
generation using Large Language Models. Supports detailed control over photography,
cinematography, composition, and artistic style.
"""

from .llm import create_openrouter_llm, image_to_base64, run_llm
from .prompt.creation import create_image_prompt_template, create_video_prompt_template
from .prompt.parser import reponse_to_string
from .schema import (
    AspectRatio,
    CameraMovement,
    ImagePrompt,
    LensType,
    LightingType,
    PhotographyType,
    ShotType,
    VideoPrompt,
)

__version__ = "0.1.0"
__author__ = "Visual Prompting Team"
__email__ = "contact@visualprompting.ai"

__all__ = [
    # Core functionality
    "run_llm",
    "create_openrouter_llm",
    "image_to_base64",
    # Schema classes
    "ImagePrompt",
    "VideoPrompt",
    # Enums
    "AspectRatio",
    "ShotType",
    "CameraMovement",
    "PhotographyType",
    "LensType",
    "LightingType",
    # Prompt utilities
    "create_image_prompt_template",
    "create_video_prompt_template",
    "reponse_to_string",
]
