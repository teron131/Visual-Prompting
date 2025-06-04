import base64
import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
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
    user_request: str,
    media_type: str = "image",
    model: str = "openai/gpt-4.1-mini",
    image_path: Optional[str] = None,
    return_string: bool = False,
) -> Union[ImagePrompt, VideoPrompt, str]:
    """Generate structured prompt using ChatPromptTemplate and OpenRouter LLM.

    Args:
        user_request: User's description or request for media generation
        media_type: Either "image" or "video"
        model: OpenRouter model to use
        image_path: Optional reference image path
        return_string: If True, return optimized string prompt instead of structured object

    Returns:
        Structured ImagePrompt/VideoPrompt object or optimized string prompt
    """
    if media_type not in ("image", "video"):
        raise ValueError("media_type must be 'image' or 'video'")

    llm = create_openrouter_llm(model)
    if media_type == "image":
        template = create_image_prompt_template()
        response_class = ImagePrompt
    else:
        template = create_video_prompt_template()
        response_class = VideoPrompt

    formatted_prompt = template.format_messages(
        media_type=media_type,
        user_request=user_request,
    )

    if image_path:
        image_base64 = image_to_base64(image_path)
        human_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            },
            {
                "type": "text",
                "text": f"Create a {media_type} generation prompt based on this request: {user_request}",
            },
        ]
        formatted_prompt[-1] = HumanMessage(content=human_content)

    structured_llm = llm.with_structured_output(
        response_class,
        method="function_calling",
    )

    structured_result = structured_llm.invoke(formatted_prompt)

    if return_string:
        return reponse_to_string(structured_result)

    return structured_result
