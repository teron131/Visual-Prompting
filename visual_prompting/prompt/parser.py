from typing import Union

from ..schema import ImagePrompt, VideoPrompt


def reponse_to_string(prompt: Union[ImagePrompt, VideoPrompt]) -> str:
    """Convert structured prompt object to optimized single string prompt.

    Args:
        prompt: ImagePrompt or VideoPrompt object from LLM

    Returns:
        Optimized single string prompt ready for AI generation
    """
    parts = []

    if isinstance(prompt, ImagePrompt):
        # Core subject and scene (most important)
        if prompt.subject:
            parts.append(prompt.subject)

        if prompt.scene_description:
            parts.append(prompt.scene_description)

        # Photography style and technical specs
        if prompt.photography_type:
            parts.append(f"{prompt.photography_type} photography")

        if prompt.artistic_style:
            parts.append(prompt.artistic_style)

        # Camera and lens specifications
        camera_specs = []
        if prompt.lens_type:
            camera_specs.append(f"{prompt.lens_type} lens")
        if prompt.focal_length:
            camera_specs.append(f"{prompt.focal_length}")
        if prompt.camera_settings:
            camera_specs.append(prompt.camera_settings)
        if camera_specs:
            parts.append(", ".join(camera_specs))

        # Lighting and atmosphere
        if prompt.lighting_type:
            if prompt.lighting_description:
                parts.append(f"{prompt.lighting_type}, {prompt.lighting_description}")
            else:
                parts.append(f"{prompt.lighting_type} lighting")
        elif prompt.lighting_description:
            parts.append(prompt.lighting_description)

        # Composition and framing
        composition_parts = []
        if prompt.shot_type:
            composition_parts.append(prompt.shot_type.replace("_", " "))
        if prompt.composition_technique:
            composition_parts.append(prompt.composition_technique)
        if composition_parts:
            parts.append(", ".join(composition_parts))

        # Color and mood
        if prompt.color_palette:
            parts.append(prompt.color_palette)

        if prompt.mood_and_emotion:
            parts.append(prompt.mood_and_emotion)

        # Quality and style references
        if prompt.image_quality and prompt.image_quality != "standard":
            parts.append(f"{prompt.image_quality} quality")

        if prompt.style_reference:
            parts.append(f"in the style of {prompt.style_reference}")

    elif isinstance(prompt, VideoPrompt):
        # Core required elements
        if prompt.subject:
            parts.append(prompt.subject)

        if prompt.action:
            parts.append(prompt.action)

        if prompt.context:
            parts.append(prompt.context)

        # Camera movement and composition
        camera_parts = []
        if prompt.camera_movement and prompt.camera_movement != "static":
            camera_parts.append(f"{prompt.camera_movement} camera movement")
        if prompt.camera_description:
            camera_parts.append(prompt.camera_description)
        if prompt.shot_type:
            camera_parts.append(prompt.shot_type.replace("_", " "))
        if prompt.composition:
            camera_parts.append(prompt.composition)
        if camera_parts:
            parts.append(", ".join(camera_parts))

        # Lighting and ambiance
        lighting_parts = []
        if prompt.lighting:
            lighting_parts.append(prompt.lighting)
        if prompt.ambiance:
            lighting_parts.append(prompt.ambiance)
        if lighting_parts:
            parts.append(", ".join(lighting_parts))

        # Style and emotion
        if prompt.style:
            parts.append(prompt.style)

        if prompt.emotional_tone:
            parts.append(f"{prompt.emotional_tone} tone")

        # Motion characteristics
        if prompt.motion_intensity and prompt.motion_intensity != "moderate":
            parts.append(f"{prompt.motion_intensity} motion")

        if prompt.duration_preference and prompt.duration_preference != "medium":
            parts.append(f"{prompt.duration_preference} duration")

        # Style reference
        if prompt.reference_style:
            parts.append(f"in the style of {prompt.reference_style}")

    # Join all parts with appropriate separators
    optimized_prompt = ", ".join(part.strip() for part in parts if part and part.strip())

    # Add negative prompt if specified
    if hasattr(prompt, "negative_prompt") and prompt.negative_prompt:
        optimized_prompt += f" --negative {prompt.negative_prompt}"

    # Add aspect ratio if not default
    if hasattr(prompt, "aspect_ratio") and prompt.aspect_ratio:
        if (isinstance(prompt, ImagePrompt) and prompt.aspect_ratio != "16:9") or (isinstance(prompt, VideoPrompt) and prompt.aspect_ratio != "16:9"):
            optimized_prompt += f" --ar {prompt.aspect_ratio}"

    return optimized_prompt
