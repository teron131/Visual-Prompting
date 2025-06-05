import base64
import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .prompt.creation import create_image_prompt_template, create_video_prompt_template
from .prompt.parser import reponse_to_string
from .schema import ImagePrompt, VideoPrompt

load_dotenv()


def image_to_base64(image_path: str) -> str:
    """Load image from path and convert to base64 mime data.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded image string
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode("utf-8")

    return base64_encoded


def create_openrouter_llm(model: str = "openai/gpt-4.1-mini") -> ChatOpenAI:
    """Create OpenRouter LLM client.

    Args:
        model: Model name to use

    Returns:
        Configured ChatOpenAI client for OpenRouter
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def run_llm(
    user_request: Optional[str] = None,
    media_type: str = "image",
    model: str = "openai/gpt-4.1-mini",
    image_path: Optional[str] = None,
    return_string: bool = False,
) -> Union[ImagePrompt, VideoPrompt, str]:
    """Generate structured prompt using system prompts and OpenRouter LLM.

    Args:
        user_request: Optional user's description or request for media generation
        media_type: Either "image" or "video"
        model: OpenRouter model to use
        image_path: Optional reference image path
        return_string: If True, return optimized string prompt instead of structured object

    Returns:
        Structured ImagePrompt/VideoPrompt object or optimized string prompt

    Raises:
        ValueError: If neither user_request nor image_path is provided
    """
    if media_type not in ("image", "video"):
        raise ValueError("media_type must be 'image' or 'video'")

    # Validate that at least one input is provided
    if not user_request and not image_path:
        raise ValueError("Either user_request or image_path must be provided")

    llm = create_openrouter_llm(model)

    # Get the appropriate SystemPrompt and response class
    if media_type == "image":
        system_prompt = create_image_prompt_template()
        response_class = ImagePrompt
    else:
        system_prompt = create_video_prompt_template()
        response_class = VideoPrompt

    messages = [SystemMessage(content=system_prompt)]

    # Create HumanMessage
    content = [
        {
            "type": "text",
            "text": f"Create a {media_type} generation prompt based on this request: {user_request}" if user_request else "Reverse engineer the image and create a prompt for generating it",
        },
    ]

    # Create human message based on whether we have an image or not
    if image_path:
        image_base64 = image_to_base64(image_path)
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            }
        )

    messages.append(HumanMessage(content=content))

    # Create structured LLM and invoke
    structured_llm = llm.with_structured_output(
        response_class,
        method="function_calling",
    )

    structured_result = structured_llm.invoke(messages)

    if return_string:
        return reponse_to_string(structured_result)

    return structured_result
