import re
from typing import Union, get_type_hints

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..schema import ImagePrompt, VideoPrompt

# =============================================================================
# FIELD DESCRIPTION EXTRACTION
# =============================================================================


def get_enum_choices(enum_class) -> str:
    """Extract enum choices with their specific descriptions from comments."""
    choices = []
    try:
        import inspect

        source_lines = inspect.getsource(enum_class).split("\n")

        for item in enum_class:
            comment = ""
            # Look for the line with this enum value and extract its comment
            for line in source_lines:
                if f'= "{item.value}"' in line and "#" in line:
                    comment = line.split("#", 1)[1].strip()
                    break

            if not comment:
                # Fallback to a descriptive name if no comment found
                comment = f"Option for {enum_class.__name__.replace('Type', '').lower()}"

            choices.append(f"  • {item.value}: {comment}")
    except:
        # Fallback if source inspection fails
        for item in enum_class:
            choices.append(f"  • {item.value}: Option for {enum_class.__name__.lower()}")

    return "\n".join(choices)


def extract_examples_from_description(description: str) -> tuple[str, list[str]]:
    """Extract examples from field description and return clean description + examples.

    Args:
        description: Field description that may contain examples

    Returns:
        Tuple of (clean_description, examples_list)
    """
    # Pattern to match "Examples: 'example1', 'example2', 'example3'"
    # This captures everything from "Examples:" to the end of the string
    examples_pattern = r"Examples?:\s*(.+?)(?:\"|$)"

    examples = []
    clean_description = description

    match = re.search(examples_pattern, description, re.IGNORECASE | re.DOTALL)
    if match:
        examples_text = match.group(1)
        # Extract quoted examples
        quote_pattern = r"'([^']+)'"
        examples = re.findall(quote_pattern, examples_text)

        # Remove the examples section from description
        clean_description = re.sub(examples_pattern, "", description, flags=re.IGNORECASE | re.DOTALL).strip()
        # Clean up any trailing periods or commas
        clean_description = re.sub(r"[,\s]+$", "", clean_description)

    return clean_description, examples


def get_comprehensive_field_description(field_info: FieldInfo, field_name: str, field_type) -> str:
    """Extract comprehensive field description with examples, constraints, and choices."""
    desc_parts = []

    # Extract and format basic description with examples
    if field_info.description:
        clean_desc, examples = extract_examples_from_description(field_info.description)
        desc_parts.append(clean_desc)

        if examples:
            desc_parts.append(f"\n**Examples:**")
            for example in examples:
                desc_parts.append(f"  - {example}")

    # Add enum choices if applicable
    if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
        # Handle Optional types
        actual_type = next(arg for arg in field_type.__args__ if arg is not type(None))
        if hasattr(actual_type, "__members__"):  # It's an enum
            desc_parts.append(f"\n**Available choices:**")
            desc_parts.append(get_enum_choices(actual_type))
    elif hasattr(field_type, "__members__"):  # Direct enum
        desc_parts.append(f"\n**Available choices:**")
        desc_parts.append(get_enum_choices(field_type))

    # Add constraints
    constraints = []
    if hasattr(field_info, "constraints"):
        # Pydantic V2 style constraints
        constraints_obj = field_info.constraints
        for constraint in constraints_obj:
            if hasattr(constraint, "min_length") and constraint.min_length:
                constraints.append(f"minimum {constraint.min_length} characters")
            if hasattr(constraint, "max_length") and constraint.max_length:
                constraints.append(f"maximum {constraint.max_length} characters")
    else:
        # Pydantic V1 style constraints
        if hasattr(field_info, "min_length") and field_info.min_length:
            constraints.append(f"minimum {field_info.min_length} characters")
        if hasattr(field_info, "max_length") and field_info.max_length:
            constraints.append(f"maximum {field_info.max_length} characters")

    if constraints:
        desc_parts.append(f"\n**Constraints:** {', '.join(constraints)}")

    return "\n".join(desc_parts)


def get_type_name(field_type) -> str:
    """Get a clean type name for display."""
    if hasattr(field_type, "__name__"):
        return field_type.__name__
    elif hasattr(field_type, "__origin__"):
        if field_type.__origin__ is Union:
            # Handle Optional types
            non_none_types = [arg for arg in field_type.__args__ if arg is not type(None)]
            if non_none_types:
                return f"Optional[{get_type_name(non_none_types[0])}]"
        return str(field_type)
    else:
        return str(field_type)


def get_schema_example(prompt_class: BaseModel) -> dict:
    """Extract example from schema configuration."""
    # Try V1 style Config class first
    if hasattr(prompt_class, "Config"):
        config_class = prompt_class.Config
        if hasattr(config_class, "json_schema_extra") and isinstance(config_class.json_schema_extra, dict):
            return config_class.json_schema_extra.get("example", {})
        if hasattr(config_class, "json_schema_extra") and isinstance(config_class.json_schema_extra, dict):
            return config_class.json_schema_extra.get("example", {})

    # Try V2 style model_config
    if hasattr(prompt_class, "model_config"):
        model_config = prompt_class.model_config
        if isinstance(model_config, dict):
            json_schema_extra = model_config.get("json_schema_extra", {})
            if isinstance(json_schema_extra, dict):
                return json_schema_extra.get("example", {})
            json_schema_extra = model_config.get("json_schema_extra", {})
            if isinstance(json_schema_extra, dict):
                return json_schema_extra.get("example", {})

    return {}


def format_example_section(example: dict) -> str:
    """Format the example section for the prompt template."""
    if not example:
        return ""

    example_lines = []
    for key, value in example.items():
        # Escape quotes and handle string values properly
        escaped_value = str(value).replace('"', '\\"')
        example_lines.append(f'  "{key}": "{escaped_value}"')

    # Use double braces to escape them in the f-string template and add proper commas
    json_content = ",\n".join(example_lines)
    return f"""

## Working Example
Here's a complete example showing professional-quality field completion:

```json
{{{{
{json_content}
}}}}
```

Use this as a reference for the level of detail and professional terminology expected."""


# =============================================================================
# PROMPT TEMPLATE GENERATION
# =============================================================================


def create_image_prompt_template() -> str:
    """Create a comprehensive system prompt for generating structured image prompts."""

    # Get model fields and type hints (Pydantic V2 compatible)
    model_fields = getattr(ImagePrompt, "model_fields", getattr(ImagePrompt, "__fields__", {}))
    type_hints = get_type_hints(ImagePrompt)

    # Organize fields by requirement and category
    required_fields = []
    optional_fields = []

    for field_name, field_info in model_fields.items():
        field_type = type_hints.get(field_name, str)

        # Determine if field is required (Fixed for Pydantic V2)
        is_required = False
        if hasattr(field_info, "is_required"):
            # Pydantic V2 method
            is_required = field_info.is_required()
        elif hasattr(field_info, "default") and hasattr(field_info, "default_factory"):
            # Pydantic V1 method
            is_required = field_info.default is ... and field_info.default_factory is None
        else:
            # Fallback - check if default is Ellipsis
            is_required = getattr(field_info, "default", None) is ...

        # Get comprehensive description with examples
        desc = get_comprehensive_field_description(field_info, field_name, field_type)

        # Format field entry with cleaner styling (removed redundant info)
        if is_required:
            field_entry = f"""### {field_name.replace('_', ' ').title()}
**Required Field**

{desc}

---
"""
            required_fields.append(field_entry)
        else:
            field_entry = f"""### {field_name.replace('_', ' ').title()}
**Optional Field**

{desc}

---
"""
            optional_fields.append(field_entry)

    # Get working example from schema
    example = get_schema_example(ImagePrompt)
    example_section = format_example_section(example) if example else ""

    # Build required fields section
    required_section = ""
    if required_fields:
        required_section = f"""## Required Fields
These fields are essential for every image generation prompt:

{chr(10).join(required_fields)}"""
    else:
        required_section = "## Required Fields\nAll fields are optional - use the most relevant ones for your specific request.\n"

    # Image-specific best practices
    technical_guidance = """
## Professional Image Generation Best Practices

### Core Structure (Subject + Context + Style)
- **Subject**: The main object, person, animal, or scenery (be specific and descriptive)
- **Context**: Background and environment where subject is placed
- **Style**: General (painting, photograph) or specific (pastel painting, film noir)

### Photography Quality Modifiers
- **General**: high-quality, beautiful, stylized, professional, detailed
- **Technical**: 4K, HDR, studio photo, sharp focus, bokeh, portrait mode
- **Artistic**: by a professional photographer, award-winning photography

### Photography Technical Specifications
**For Portraits**: 24-35mm lens, shallow depth of field, prime/zoom lens, film noir style
**For Objects/Still Life**: 60-105mm macro lens, high detail, precise focusing, controlled lighting
**For Motion**: 100-400mm telephoto, fast shutter speed, action tracking
**For Landscapes**: 10-24mm wide-angle, long exposure, sharp focus throughout

### Lighting Modifiers
- **Natural**: sunlight, golden hour, blue hour, ambient lighting
- **Artificial**: studio lighting, soft box, hard light, ring light
- **Creative**: backlighting, side lighting, candlelight, neon lighting

### Camera Settings for Photorealism
Include specific technical settings like:
- f/1.4 (shallow depth of field), f/8 (sharp focus throughout)
- 1/500s (fast shutter), ISO 100 (minimal noise)
- 85mm portrait lens, 35mm street photography"""

    negative_prompt_guidance = """
### Negative Prompts
✅ **Do**: Describe what you don't want plainly (e.g., "blurry, overexposed, distorted")
❌ **Don't**: Use instructive language ("no", "don't show", "avoid")"""

    # Create comprehensive system message with professional best practices
    system_content = f"""You are an expert image generation prompt engineer specializing in AI-powered content creation. Transform user requests into professional-quality prompts following industry standards and best practices.

## Your Mission
Analyze user input and create a comprehensive {ImagePrompt.__name__} structure. Apply professional-level detail, technical accuracy, and creative enhancement based on modern AI generation capabilities.

{required_section}

## Optional Enhancement Fields
Use these fields to elevate prompt quality and match user intent:

{chr(10).join(optional_fields)}

{technical_guidance}

{negative_prompt_guidance}

## Professional Guidelines

### 1. Descriptive Precision (Industry Standard)
- Use detailed adjectives and adverbs for clear AI understanding
- Include background context when necessary
- Reference specific artists/styles for particular aesthetics
- Be specific rather than generic ("confident business executive" vs "nice person")

### 2. Technical Excellence
- Apply industry-standard image production techniques
- Use proper terminology for camera, lighting, and composition
- Consider modern AI generation capabilities and limitations
- Include relevant technical specifications

### 3. Creative Enhancement
- Expand user input with professional artistic details
- Add atmospheric and stylistic elements following industry guidelines
- Balance creative vision with technical feasibility
- Consider mood, emotion, and visual impact

### 4. Structured Approach
- Ensure all fields work harmoniously together
- Maintain consistency in style and tone across fields
- Follow the core structure: Subject + Context + Style + Technical specs
- Optimize for current AI generation capabilities

### 5. Quality Optimization
- Consider intended use case and audience
- Include appropriate quality modifiers
- Apply suitable aspect ratios and technical settings
- Balance detail with clarity (avoid over-complexity){example_section}

## Response Requirements
Return a valid JSON object matching the {ImagePrompt.__name__} structure exactly. Include all required fields and relevant optional fields based on user request, creative vision, and industry best practices."""

    return system_content


def create_video_prompt_template() -> str:
    """Create a comprehensive system prompt for generating structured video prompts."""

    # Get model fields and type hints (Pydantic V2 compatible)
    model_fields = getattr(VideoPrompt, "model_fields", getattr(VideoPrompt, "__fields__", {}))
    type_hints = get_type_hints(VideoPrompt)

    # Organize fields by requirement and category
    required_fields = []
    optional_fields = []

    for field_name, field_info in model_fields.items():
        field_type = type_hints.get(field_name, str)

        # Determine if field is required (Fixed for Pydantic V2)
        is_required = False
        if hasattr(field_info, "is_required"):
            # Pydantic V2 method
            is_required = field_info.is_required()
        elif hasattr(field_info, "default") and hasattr(field_info, "default_factory"):
            # Pydantic V1 method
            is_required = field_info.default is ... and field_info.default_factory is None
        else:
            # Fallback - check if default is Ellipsis
            is_required = getattr(field_info, "default", None) is ...

        # Get comprehensive description with examples
        desc = get_comprehensive_field_description(field_info, field_name, field_type)

        # Format field entry with cleaner styling (removed redundant info)
        if is_required:
            field_entry = f"""### {field_name.replace('_', ' ').title()}
**Required Field**

{desc}

---
"""
            required_fields.append(field_entry)
        else:
            field_entry = f"""### {field_name.replace('_', ' ').title()}
**Optional Field**

{desc}

---
"""
            optional_fields.append(field_entry)

    # Get working example from schema
    example = get_schema_example(VideoPrompt)
    example_section = format_example_section(example) if example else ""

    # Build required fields section
    required_section = ""
    if required_fields:
        required_section = f"""## Required Fields
These fields are essential for every video generation prompt:

{chr(10).join(required_fields)}"""
    else:
        required_section = "## Required Fields\nAll fields are optional - use the most relevant ones for your specific request.\n"

    # Video-specific best practices
    technical_guidance = """
## Professional Video Generation Best Practices

### Essential Elements for Video Generation
1. **Subject**: Object, person, animal, or scenery you want
2. **Context**: Background/environment where subject is placed  
3. **Action**: What the subject is doing (walking, running, turning head)
4. **Style**: Film style (horror film, film noir) or animation (cartoon style)
5. **Camera Motion**: Aerial view, eye-level, tracking shot, dolly movement
6. **Composition**: Wide shot, close-up, extreme close-up framing
7. **Ambiance**: Color/lighting (blue tones, warm tones, golden hour)

### Video Generation Principles
**Power of Simplicity**: Often less is more - let AI fill in contextually appropriate details
**Camera Movements**: static, pan, tilt, zoom in/out, dolly, tracking, handheld, drone, crane
**Quality**: Smooth motion, cinematic look, specific film references

### Camera Specifications for Video
- **POV shots**: First-person perspective, immersive experience
- **Aerial views**: Drone shots, bird's eye perspective, tracking drone view
- **Tracking shots**: Follow subject movement, smooth camera motion
- **Composition**: Wide shot (full environment), close-up (facial details), extreme close-up (specific details)

### Ambiance & Color Palettes
- **Warm tones**: muted orange warm tones, golden hour, sunrise/sunset
- **Cool tones**: pastel blue and pink tones, cool blue tones, night atmosphere
- **Lighting**: natural light, dim ambient lighting, dramatic lighting, soft lighting

### Audio Considerations (if supported)
Clearly specify audio requirements in separate sentences:
- **Sound effects**: "The audio features water splashing in the background"
- **Music**: "Add soft music in the background"
- **Speech**: Character dialogue with clear speaker identification"""

    negative_prompt_guidance = """
### Negative Prompts
✅ **Do**: Describe unwanted elements plainly (e.g., "urban background, dark atmosphere")
❌ **Don't**: Use instructive language ("no walls", "don't show buildings")

### Multiple Characters (Image-to-Video)
When multiple subjects present, use distinguishing details:
- "The man in the red hat" + "The woman in the blue dress"
- Ensure actions align with each character in the input image"""

    # Create comprehensive system message with professional best practices
    system_content = f"""You are an expert video generation prompt engineer specializing in AI-powered content creation. Transform user requests into professional-quality prompts following industry standards and best practices.

## Your Mission
Analyze user input and create a comprehensive {VideoPrompt.__name__} structure. Apply professional-level detail, technical accuracy, and creative enhancement based on modern AI generation capabilities.

{required_section}

## Optional Enhancement Fields
Use these fields to elevate prompt quality and match user intent:

{chr(10).join(optional_fields)}

{technical_guidance}

{negative_prompt_guidance}

## Professional Guidelines

### 1. Descriptive Precision (Industry Standard)
- Use detailed adjectives and adverbs for clear AI understanding
- Include background context when necessary
- Reference specific artists/styles for particular aesthetics
- Be specific rather than generic ("confident business executive" vs "nice person")

### 2. Technical Excellence
- Apply industry-standard video production techniques
- Use proper terminology for camera, lighting, and composition
- Consider modern AI generation capabilities and limitations
- Include relevant technical specifications

### 3. Creative Enhancement
- Expand user input with professional artistic details
- Add atmospheric and stylistic elements following industry guidelines
- Balance creative vision with technical feasibility
- Consider mood, emotion, and visual impact

### 4. Structured Approach
- Ensure all fields work harmoniously together
- Maintain consistency in style and tone across fields
- Follow the core structure: Subject + Context + Style + Technical specs
- Optimize for current AI generation capabilities

### 5. Quality Optimization
- Consider intended use case and audience
- Include appropriate quality modifiers
- Apply suitable aspect ratios and technical settings
- Balance detail with clarity (avoid over-complexity){example_section}

## Response Requirements
Return a valid JSON object matching the {VideoPrompt.__name__} structure exactly. Include all required fields and relevant optional fields based on user request, creative vision, and industry best practices."""

    return system_content
