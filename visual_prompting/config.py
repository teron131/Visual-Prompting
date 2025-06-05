"""Configuration management for Visual Prompting package."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Package Information
PACKAGE_NAME = "visual-prompting"
VERSION = "0.1.0"

# Environment Settings
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4.1-mini")

# File Paths
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / ".cache"
LOGS_DIR = PROJECT_ROOT / "logs"
UPLOADS_DIR = CACHE_DIR / "upload"

# Feature Flags
ENABLE_IMAGE_UPLOAD = os.getenv("ENABLE_IMAGE_UPLOAD", "true").lower() == "true"
ENABLE_VIDEO_PROMPTS = os.getenv("ENABLE_VIDEO_PROMPTS", "true").lower() == "true"

# Prompt Generation Settings
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "2000"))
DEFAULT_ASPECT_RATIO = os.getenv("DEFAULT_ASPECT_RATIO", "16:9")


def validate_config():
    """Validate configuration and create required directories."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    # Create directories if they don't exist
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
