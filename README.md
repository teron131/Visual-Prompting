# Visual Prompting

AI-powered structured prompt generation for visual media creation. Generate detailed, professional prompts for image and video generation using Large Language Models.

This library generates structured outputs according to industry-standard prompting guides:

**Image Generation Guides:**
- [Runway Gen-4 Image Prompting Guide](https://help.runwayml.com/hc/en-us/articles/35694045317139-Gen-4-Image-Prompting-Guide)
- [Google Vertex AI Image Generation Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide)

**Video Generation Guides:**
- [Runway Gen-4 Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)
- [Google Vertex AI Image Generation Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide)

## Installation

```bash
pip install -e .
```

## Setup

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_key_here
DEFAULT_MODEL=openai/gpt-4.1-mini
```

## Usage

```python
from visual_prompting import run_llm

# Generate structured image prompt
result = run_llm(
    user_request="A professional headshot",
    media_type="image"
)

# Generate optimized string prompt
prompt = run_llm(
    user_request="A professional headshot",
    media_type="image", 
    return_string=True
)

# Generate video prompt
video_result = run_llm(
    user_request="A cat playing with yarn",
    media_type="video"
)
```

## License

MIT License 