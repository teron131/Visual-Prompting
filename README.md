# Visual Prompting Studio 🎨

AI-powered structured prompt generation for visual media. Create professional prompts for image and video generation using advanced language models.

![Visual Prompting Studio](https://img.shields.io/badge/Visual-Prompting-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-red?style=for-the-badge)

## ✨ Features

- **🖼️ Image Prompts**: Generate detailed prompts for image generation with photography controls
- **🎬 Video Prompts**: Create cinematic prompts for video generation with camera movement
- **📸 Image Upload**: Analyze reference images to enhance prompt generation
- **🎛️ Advanced Controls**: Control aspect ratios, photography types, lighting, and more
- **🔢 Batch Generation**: Generate 1-4 prompts at once
- **🌐 Web Interface**: Beautiful, modern web UI with real-time generation
- **📝 Structured Output**: Professional-grade prompts using industry standards

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd Visual-Prompting
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 3. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Add your API keys:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEFAULT_MODEL=openai/gpt-4-mini
DEBUG=false
```

### 4. Start the Application

#### Option A: Simple Start (Backend Only)
```bash
./start.sh
```

#### Option B: Full-Stack Development
```bash
# Install frontend dependencies
npm run setup

# Start both backend and frontend
npm run dev
```

### 5. Access the Interface

- **Web UI**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## 🎯 Usage

### Web Interface

1. **Choose Mode**: Select between Image or Video generation
2. **Enter Prompt**: Describe what you want to create
3. **Upload Reference** (Optional): Add an image for context
4. **Set Output Count**: Choose 1-4 prompts to generate
5. **Generate**: Click generate to create structured prompts
6. **Copy Results**: Use the copy button to get your prompts

### API Usage

#### Generate Image Prompts
```python
import requests

response = requests.post("http://localhost:8001/api/generate", json={
    "mode": "image",
    "text_input": "A serene mountain landscape at sunset",
    "num_outputs": 2
})

prompts = response.json()["prompts"]
```

#### Generate with Image Reference
```python
import requests

files = {"image": open("reference.jpg", "rb")}
data = {
    "mode": "image",
    "text_input": "Create a similar scene but with different lighting",
    "num_outputs": 1
}

response = requests.post("http://localhost:8001/api/generate-with-image", 
                        files=files, data=data)
```

### Python Package Usage

```python
from visual_prompting import (
    create_openrouter_llm,
    create_image_prompt_template,
    run_llm,
    reponse_to_string
)

# Create LLM client
llm = create_openrouter_llm()

# Generate image prompt
template = create_image_prompt_template("A beautiful sunset over mountains")
response = run_llm(llm, template, None)
prompt = reponse_to_string(response)

print(prompt)
```

## 🏗️ Project Structure

```
Visual-Prompting/
├── visual_prompting/          # Core Python package
│   ├── __init__.py
│   ├── app.py                # FastAPI application
│   ├── config.py             # Configuration management
│   ├── schema.py             # Pydantic models and enums
│   ├── llm.py                # LLM integration
│   └── prompt/               # Prompt generation modules
├── visual-prompting-ui/      # Frontend (React/Next.js)
│   ├── simple-ui.html        # Simple HTML interface
│   ├── package.json
│   └── app/                  # Next.js app (future)
├── start.sh                  # Backend startup script
├── package.json              # Root coordination
└── requirements.txt          # Python dependencies
```

## 🎨 Supported Features

### Image Generation
- **Photography Types**: Portrait, Landscape, Macro, Street, Product, etc.
- **Lens Types**: Wide-angle, Portrait, Telephoto, Macro, Fisheye
- **Lighting**: Natural, Golden hour, Studio, Neon, Candlelight
- **Shot Types**: Close-up, Wide shot, Bird's eye, Low angle
- **Aspect Ratios**: Square (1:1), Widescreen (16:9), Portrait (9:16), etc.

### Video Generation
- **Camera Movements**: Static, Pan, Tilt, Zoom, Dolly, Tracking, Drone
- **Shot Types**: All image shot types plus cinematic movements
- **Duration Control**: Short, Medium, Long sequences
- **Motion Intensity**: Subtle, Moderate, Dynamic, Intense

## 🔧 Configuration

### Environment Variables

```env
# Required
OPENROUTER_API_KEY=your_api_key

# Optional
DEFAULT_MODEL=openai/gpt-4-mini
DEBUG=false
HOST=localhost
PORT=8001
MAX_PROMPT_LENGTH=2000
DEFAULT_ASPECT_RATIO=16:9
ENABLE_IMAGE_UPLOAD=true
ENABLE_VIDEO_PROMPTS=true
```

### Model Selection

Supported models via OpenRouter:
- `openai/gpt-4-mini` (default)
- `openai/gpt-4`
- `anthropic/claude-3-haiku`
- `anthropic/claude-3-sonnet`

## 📖 API Reference

### Endpoints

- `GET /` - Web interface
- `POST /api/generate` - Generate prompts
- `POST /api/generate-with-image` - Generate with image reference
- `GET /api/enums` - Get available enum values
- `GET /docs` - API documentation

### Response Format

```json
{
  "status": "success",
  "prompts": [
    "A serene mountain landscape at golden hour, captured with a wide-angle lens..."
  ],
  "mode": "image",
  "num_outputs": 1
}
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone <repo-url>
cd Visual-Prompting

# Install in development mode
pip install -e .

# Install pre-commit hooks (optional)
pre-commit install
```

### Running Tests

```bash
# Run Python tests
pytest

# Run with coverage
pytest --cov=visual_prompting
```

### Code Style

This project follows Python coding standards:
- Type annotations required
- Pydantic for data validation
- FastAPI for API endpoints
- Comprehensive error handling

## 📝 Examples

### Example Generated Prompts

**Image Prompt:**
```
A professional woman in her 30s wearing a navy blazer with confident expression, in a modern minimalist office with floor-to-ceiling windows overlooking a city skyline during golden hour. Photography style: contemporary corporate portrait with cinematic quality. Camera: 85mm portrait lens, f/2.8 shallow depth of field. Lighting: warm golden light streaming through windows creating soft highlights on her face. Composition: rule of thirds with subject positioned on right intersection. Colors: warm golden tones with deep blue accents from the cityscape. Mood: confident and professional with approachable warmth.
```

**Video Prompt:**
```
A golden retriever with a red collar runs joyfully toward the camera with tongue hanging out, in a sunlit meadow filled with wildflowers during golden hour. Camera movement: smooth tracking shot following the dog's movement. Style: cinematic documentary with warm color grading. Shot type: medium-wide shot capturing both the dog and beautiful environment. Lighting: warm golden hour sunlight with soft shadows. Duration: 8-10 seconds of energetic movement. Mood: joyful and energetic with natural outdoor atmosphere.
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI and modern web technologies
- Powered by OpenRouter for LLM access
- Inspired by professional photography and cinematography standards

---

**Happy prompting! 🎨✨** 