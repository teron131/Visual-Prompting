from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field

# =============================================================================
# SHARED ENUMS
# =============================================================================


class AspectRatio(str, Enum):
    """Supported aspect ratios for media generation."""

    SQUARE = "1:1"  # Perfect for social media, profile pictures, product shots
    WIDESCREEN = "16:9"  # Landscape, ideal for TVs, monitors, scenic landscapes
    PORTRAIT = "9:16"  # Portrait, ideal for mobile, social media, tall objects
    CLASSIC = "4:3"  # Traditional photography ratio
    ULTRAWIDE = "21:9"  # Cinematic ultrawide format
    GOLDEN = "3:2"  # Golden ratio, natural photography


class ShotType(str, Enum):
    """Common shot compositions and framing types."""

    EXTREME_WIDE = "extreme_wide_shot"  # Shows entire environment, subjects are small
    WIDE = "wide_shot"  # Shows full subject and surroundings
    MEDIUM_WIDE = "medium_wide_shot"  # Shows subject from knees up
    MEDIUM = "medium_shot"  # Shows subject from waist up
    MEDIUM_CLOSE = "medium_close_up"  # Shows subject from chest up
    CLOSE_UP = "close_up"  # Shows subject's face and shoulders
    EXTREME_CLOSE_UP = "extreme_close_up"  # Shows specific details, eyes, hands
    BIRD_EYE = "bird_eye_view"  # High overhead perspective
    LOW_ANGLE = "low_angle"  # Camera below subject, looking up
    HIGH_ANGLE = "high_angle"  # Camera above subject, looking down
    EYE_LEVEL = "eye_level"  # Camera at subject's eye level


# =============================================================================
# VIDEO-SPECIFIC ENUMS
# =============================================================================


class CameraMovement(str, Enum):
    """Common camera movement types for video."""

    STATIC = "static"  # Camera remains stationary
    PAN = "pan"  # Horizontal camera rotation
    TILT = "tilt"  # Vertical camera rotation
    ZOOM_IN = "zoom_in"  # Lens zooms closer to subject
    ZOOM_OUT = "zoom_out"  # Lens zooms away from subject
    DOLLY = "dolly"  # Camera moves physically closer/farther
    TRACKING = "tracking"  # Camera follows subject movement
    HANDHELD = "handheld"  # Natural camera shake, documentary style
    DRONE = "drone"  # Aerial perspective with smooth movement
    CRANE = "crane"  # High sweeping movements, cinematic


# =============================================================================
# IMAGE-SPECIFIC ENUMS
# =============================================================================


class PhotographyType(str, Enum):
    """Photography types based on industry standards."""

    PORTRAIT = "portrait"  # People, characters, headshots, personality
    LANDSCAPE = "landscape"  # Natural scenery, wide vistas, outdoors
    MACRO = "macro"  # Close-up details, small subjects, textures
    STREET = "street"  # Urban, candid, documentary style
    PRODUCT = "product"  # Commercial, clean backgrounds, advertising
    ARCHITECTURAL = "architectural"  # Buildings, structures, interiors, design
    WILDLIFE = "wildlife"  # Animals in natural habitats, nature
    FOOD = "food"  # Culinary, still life, restaurant style
    FASHION = "fashion"  # Clothing, style, modeling, editorial
    ABSTRACT = "abstract"  # Artistic, conceptual, non-representational
    STUDIO = "studio"  # Controlled lighting, professional setup
    DOCUMENTARY = "documentary"  # Photojournalism, real-life events, storytelling


class LensType(str, Enum):
    """Camera lens types for specific photography effects."""

    WIDE_ANGLE = "wide_angle"  # 10-24mm, landscapes, architecture, dramatic perspective
    STANDARD = "standard"  # 35-50mm, natural perspective, everyday photography
    PORTRAIT_LENS = "portrait"  # 85-135mm, portraits, shallow DOF, compression
    TELEPHOTO = "telephoto"  # 100-400mm, sports, wildlife, distant subjects
    MACRO_LENS = "macro"  # 60-105mm, close-up details, 1:1 reproduction
    FISHEYE = "fisheye"  # Ultra-wide, distorted perspective, creative effects


class LightingType(str, Enum):
    """Lighting setup types for photography."""

    NATURAL = "natural"  # Sunlight, ambient lighting, outdoors
    GOLDEN_HOUR = "golden_hour"  # Warm, soft sunset/sunrise light
    BLUE_HOUR = "blue_hour"  # Cool twilight lighting, magical atmosphere
    STUDIO = "studio"  # Controlled artificial lighting setup
    SOFT_BOX = "soft_box"  # Diffused, even lighting, minimal shadows
    HARD_LIGHT = "hard_light"  # Sharp shadows, dramatic contrast, directional
    BACKLIGHTING = "backlighting"  # Light behind subject, rim lighting, silhouettes
    SIDE_LIGHTING = "side_lighting"  # Light from side, dramatic shadows, depth
    RING_LIGHT = "ring_light"  # Even, shadowless lighting, beauty photography
    CANDLELIGHT = "candlelight"  # Warm, intimate atmosphere, low light
    NEON = "neon"  # Colorful artificial lighting, urban night


# =============================================================================
# IMAGE PROMPT SCHEMA
# =============================================================================


class ImagePrompt(BaseModel):
    """Comprehensive image generation prompt structure.

    Based on Google Cloud Imagen and Runway guidelines for professional-quality
    image generation with detailed control over photography, composition, and style.
    """

    # CORE SUBJECT AND COMPOSITION
    subject: str = Field(..., description=("The main subject, object, person, or scene that serves as the focal point. " "Be specific and descriptive with unique characteristics. " "Examples: 'a professional woman in a navy blazer with confident expression', " "'a vintage red bicycle leaning against a weathered brick wall', " "'a golden retriever with floppy ears sitting in autumn leaves'"), min_length=5, max_length=300)

    scene_description: str = Field(..., description=("Detailed description of the setting, environment, and background context. " "Include location, time of day, weather, atmosphere, and surrounding elements. " "Examples: 'in a modern minimalist office with floor-to-ceiling windows', " "'on a misty mountain trail during sunrise', " "'in a bustling Tokyo street with neon signs reflecting on wet pavement'"), min_length=10, max_length=400)

    # PHOTOGRAPHY TECHNICAL SPECIFICATIONS
    photography_type: Optional[PhotographyType] = Field(None, description=("Type of photography style that determines overall approach and technique. " "Examples: 'portrait' for people and characters, 'landscape' for scenery, " "'macro' for close details, 'street' for urban candid shots"))

    lens_type: Optional[LensType] = Field(None, description=("Camera lens type that affects perspective, depth of field, and framing. " "Examples: 'wide_angle' for dramatic landscapes, 'portrait' for shallow DOF, " "'telephoto' for distant subjects, 'macro' for extreme close-ups"))

    focal_length: Optional[str] = Field(None, description=("Specific focal length measurement for precise lens control. " "Examples: '35mm' for street photography, '85mm' for portraits, " "'200mm' for wildlife, '14mm' for ultra-wide architecture"), max_length=20)

    # LIGHTING AND ATMOSPHERE
    lighting_type: Optional[LightingType] = Field(None, description=("Primary lighting setup and quality. " "Examples: 'golden_hour' for warm sunset light, 'studio' for controlled lighting, " "'natural' for outdoor ambient, 'backlighting' for dramatic silhouettes"))

    lighting_description: Optional[str] = Field(None, description=("Detailed lighting characteristics beyond the basic type. " "Examples: 'dramatic side lighting creating strong shadows on the left side', " "'soft diffused light from large window creating gentle highlights', " "'warm candlelight casting flickering shadows with intimate atmosphere'"), max_length=250)

    color_palette: Optional[str] = Field(None, description=("Color scheme and tonal characteristics of the image. " "Examples: 'warm earth tones with golden and brown hues', " "'monochromatic blue palette with various shades', " "'vibrant saturated colors with neon accents'"), max_length=200)

    # COMPOSITION AND FRAMING
    shot_type: Optional[ShotType] = Field(None, description=("Shot framing and camera angle. " "Examples: 'close_up' for facial details, 'wide_shot' for full environment, " "'low_angle' for powerful subjects, 'bird_eye' for overhead perspective"))

    composition_technique: Optional[str] = Field(None, description=("Artistic composition rules and framing techniques. " "Examples: 'rule of thirds with subject positioned on left intersection', " "'symmetrical composition with perfect center balance', " "'leading lines drawing viewer's eye from foreground to background'"), max_length=250)

    # ARTISTIC STYLE AND AESTHETICS
    artistic_style: Optional[str] = Field(None, description=("Artistic movement, aesthetic, or visual style inspiration. " "Examples: 'Renaissance painting style with dramatic chiaroscuro', " "'minimalist modern aesthetic with clean lines', " "'cyberpunk aesthetic with neon colors and urban decay'"), max_length=200)

    mood_and_emotion: Optional[str] = Field(None, description=("Emotional tone and psychological feeling the image should convey. " "Examples: 'serene and peaceful with calming atmosphere', " "'dramatic and intense with tension and energy', " "'nostalgic and melancholic with wistful sadness'"), max_length=150)

    # TECHNICAL IMAGE SPECIFICATIONS
    aspect_ratio: Optional[AspectRatio] = Field(AspectRatio.WIDESCREEN, description=("Image proportions for different use cases. " "Examples: '1:1' for social media posts, '16:9' for displays, " "'9:16' for mobile content, '3:2' for natural photography"))

    image_quality: Optional[Literal["standard", "high", "ultra", "artistic"]] = Field("high", description=("Image resolution and detail level. " "Examples: 'high' for detailed work, 'ultra' for maximum resolution, " "'artistic' for creative interpretation with stylization"))

    camera_settings: Optional[str] = Field(None, description=("Specific camera technical settings for photorealistic results. " "Examples: 'f/1.4 shallow depth of field', 'f/8 sharp focus throughout', " "'1/500s fast shutter speed freezing motion', 'ISO 100 minimal noise'"), max_length=200)

    # QUALITY CONTROL
    negative_prompt: Optional[str] = Field(None, description=("Visual elements to avoid or exclude from the image. " "Examples: 'blurry details, overexposed highlights, distorted proportions', " "'artificial lighting, cluttered background, poor composition'"), max_length=200)

    style_reference: Optional[str] = Field(None, description=("Reference to specific photographers, artists, films, or visual works. " "Examples: 'Annie Leibovitz portrait style', 'Ansel Adams landscape photography', " "'Blade Runner 2049 cinematography', 'Studio Ghibli animation aesthetic'"), max_length=150)

    class Config:
        """Pydantic configuration for the ImagePrompt model."""

        use_enum_values = True
        validate_assignment = True
        json_schema_extra = {"example": {"subject": "a professional woman in her 30s wearing a navy blazer with confident expression", "scene_description": "in a modern minimalist office with floor-to-ceiling windows overlooking a city skyline during golden hour", "photography_type": "portrait", "lens_type": "portrait", "focal_length": "85mm", "lighting_type": "golden_hour", "lighting_description": "warm golden light streaming through windows creating soft highlights on her face", "color_palette": "warm golden tones with deep blue accents from the cityscape", "shot_type": "medium_close_up", "composition_technique": "rule of thirds with subject positioned on right intersection", "artistic_style": "contemporary corporate portrait with cinematic quality", "mood_and_emotion": "confident and professional with approachable warmth", "aspect_ratio": "3:2", "image_quality": "high", "camera_settings": "f/2.8 shallow depth of field with sharp focus on eyes"}}


# =============================================================================
# VIDEO PROMPT SCHEMA
# =============================================================================


class VideoPrompt(BaseModel):
    """Comprehensive video generation prompt structure.

    Based on Google Cloud Veo and Runway Gen-4 guidelines for professional-quality
    video generation with detailed control over cinematography, movement, and storytelling.
    """

    # CORE REQUIRED ELEMENTS
    subject: str = Field(..., description=("The primary object, person, animal, or scenery that serves as the main focus. " "Be specific and descriptive with unique characteristics. " "Examples: 'a golden retriever with floppy ears', " "'a majestic oak tree with autumn leaves', 'a woman in a red dress'"), min_length=3, max_length=200)

    context: str = Field(..., description=("The background, setting, or environment where the action takes place. " "Include spatial relationships and environmental details. " "Examples: 'in a misty forest clearing at dawn', " "'on a busy city street during rush hour', 'inside a cozy library with warm lighting'"), min_length=5, max_length=300)

    action: str = Field(..., description=("Specific actions, movements, or behaviors the subject performs. " "Use active, concrete verbs rather than abstract concepts. " "Examples: 'walks slowly while looking over shoulder', " "'jumps with excitement, arms raised high', 'carefully paints brushstrokes on canvas'"), min_length=5, max_length=250)

    style: str = Field(..., description=("Visual and aesthetic style for the video. " "Examples: 'film noir with high contrast shadows', " "'Studio Ghibli animated style', 'cinematic horror film atmosphere', " "'1970s retro aesthetic with warm film grain'"), min_length=5, max_length=200)

    # CAMERA AND TECHNICAL ELEMENTS
    camera_movement: Optional[CameraMovement] = Field(None, description=("Type of camera movement during the shot. " "Examples: 'static' for stationary camera, 'tracking' to follow subject, " "'drone' for aerial perspectives, 'handheld' for documentary style"))

    camera_description: Optional[str] = Field(None, description=("Detailed description of camera behavior and movement. " "Examples: 'smooth dolly shot moving from left to right', " "'handheld camera with gentle natural movement', " "'static wide shot that slowly zooms into character's face'"), max_length=200)

    shot_type: Optional[ShotType] = Field(None, description=("Shot composition and framing type. " "Examples: 'wide_shot' for full environment, 'close_up' for facial details, " "'low_angle' for powerful subjects, 'bird_eye' for overhead view"))

    composition: Optional[str] = Field(None, description=("Advanced shot framing and visual composition details. " "Examples: 'rule of thirds with subject on left third', " "'symmetrical composition with centered subject', " "'shallow depth of field with blurred background'"), max_length=200)

    # LIGHTING AND ATMOSPHERE
    lighting: Optional[str] = Field(None, description=("Lighting setup, quality, and characteristics. " "Examples: 'soft golden hour lighting', 'dramatic high contrast shadows', " "'neon lighting with colored reflections', 'warm candlelight ambiance'"), max_length=200)

    ambiance: Optional[str] = Field(None, description=("Overall mood, atmosphere, and environmental feeling. " "Examples: 'warm sunset tones with orange and pink hues', " "'cool blue moonlight with misty atmosphere', " "'bright cheerful spring morning with vibrant colors'"), max_length=200)

    # TECHNICAL AND TIMING SPECIFICATIONS
    aspect_ratio: Optional[AspectRatio] = Field(AspectRatio.WIDESCREEN, description=("Video aspect ratio for different platforms. " "Examples: '16:9' for landscape/TV, '9:16' for mobile/social media, " "'1:1' for square social posts, '21:9' for cinematic ultrawide"))

    duration_preference: Optional[Literal["short", "medium", "long"]] = Field("medium", description=("Preferred video length based on content complexity. " "Examples: 'short' for quick actions (2-5s), 'medium' for standard clips (5-10s), " "'long' for complex sequences (10+ seconds)"))

    motion_intensity: Optional[Literal["subtle", "moderate", "dynamic", "intense"]] = Field("moderate", description=("Overall amount of movement and action in the video. " "Examples: 'subtle' for gentle movement, 'dynamic' for energetic action, " "'intense' for high-energy sequences with rapid changes"))

    # QUALITY AND REFINEMENT CONTROLS
    negative_prompt: Optional[str] = Field(None, description=("Elements to avoid or exclude from the video. " "Examples: 'blurry motion, camera shake, distorted faces', " "'poor lighting, choppy movement, unnatural physics'"), max_length=200)

    reference_style: Optional[str] = Field(None, description=("Reference to specific films, directors, artists, or visual styles. " "Examples: 'Blade Runner 2049 cinematography', 'Miyazaki animation style', " "'Kubrick symmetrical framing', 'David Fincher color grading'"), max_length=150)

    # NARRATIVE AND CREATIVE ELEMENTS
    transition_type: Optional[str] = Field(None, description=("How the video should begin, progress, or end if part of a sequence. " "Examples: 'fade in from black', 'seamless loop', " "'natural ending with stillness', 'dramatic reveal at climax'"), max_length=100)

    emotional_tone: Optional[str] = Field(None, description=("The emotional feeling or mood the video should convey. " "Examples: 'peaceful and serene', 'tense and suspenseful', " "'joyful and energetic', 'melancholic and contemplative'"), max_length=100)

    class Config:
        """Pydantic configuration for the VideoPrompt model."""

        use_enum_values = True
        validate_assignment = True
        json_schema_extra = {"example": {"subject": "a golden retriever with a red collar", "context": "in a sunlit meadow filled with wildflowers during golden hour", "action": "runs joyfully toward the camera with tongue hanging out", "style": "cinematic documentary style with warm color grading", "camera_movement": "tracking", "camera_description": "smooth tracking shot following the dog's movement", "shot_type": "medium_wide_shot", "lighting": "warm golden hour sunlight with soft shadows", "ambiance": "peaceful spring afternoon with gentle warm tones", "aspect_ratio": "16:9", "motion_intensity": "dynamic", "emotional_tone": "joyful and energetic"}}
