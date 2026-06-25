"""
Structured generation for the chat prompt refinement.
--------------------------------------------------------------------------------
`website.structured_generation`

"""
import os

from openai   import OpenAI
from pydantic import BaseModel, Field

# Use the OpenAI library, but pointed at Groq's OpenAI-compatible endpoint + key,
# so structured generation runs on our Groq key (no separate OpenAI key needed here).
client = OpenAI(
    base_url = "https://api.groq.com/openai/v1",
    api_key  = os.environ.get("GROQ_API_KEY"),
)

# Must be a Groq model that supports JSON-schema structured outputs. If this one
# rejects the schema, swap it for one that does -- e.g. "openai/gpt-oss-20b",
# "meta-llama/llama-4-scout-17b-16e-instruct", or "moonshotai/kimi-k2-instruct".
STRUCTURED_MODEL = "llama-3.3-70b-versatile"


# ================================================================================
# Output schemas (five named elements + a combined, ready-to-use final prompt)
# ================================================================================

# --------------------------------------------------------------------------------
# Image-refinement schema (mirrors SYSTEM_PROMPT_IMAGE)
# --------------------------------------------------------------------------------
class RefinedImagePrompt(BaseModel):
    core_subject:            str = Field(description="The primary focus, described with precise, vivid physical details.")
    medium_and_style:        str = Field(description="The specific visual format (e.g., 35mm macro photography, cyberpunk concept art, oil painting).")
    lighting_and_atmosphere: str = Field(description="The mood and illumination (e.g., volumetric lighting, golden hour, bioluminescent glow).")
    composition_and_camera:  str = Field(description="Framing and perspective (e.g., extreme close-up, low-angle shot, 24mm lens).")
    quality_and_technical:   str = Field(description="Engine and render tags (e.g., 8k resolution, intricate details, masterpiece, octane render).")
    final_prompt:            str = Field(description="The complete refined prompt as one ready-to-use, comma-separated string combining all elements above.")


# --------------------------------------------------------------------------------
# Story-refinement schema (mirrors SYSTEM_PROMPT_TEXT)
# --------------------------------------------------------------------------------
class RefinedStoryPrompt(BaseModel):
    core_narrative_arc:          str = Field(description="The immediate conflict, the climax, and the resolution/twist, compressed to fit one paragraph.")
    character_and_perspective:   str = Field(description="The focal character and the point of view (e.g., close third-person, unreliable first-person).")
    setting_and_sensory_anchors: str = Field(description="The specific environment and 1-2 distinct sensory details (smell, sound, texture).")
    tone_and_voice:              str = Field(description="The emotional atmosphere and stylistic execution (e.g., lyrical and melancholic, gritty realism).")
    structural_constraints:      str = Field(description="Instructions on pacing and structure (e.g., 'start in media res', 'end with a lingering question').")
    final_prompt:                str = Field(description="The complete refined narrative prompt as one ready-to-use string combining all elements above.")


# ================================================================================
# Structured prompt refinement (OpenAI + Pydantic)
# ================================================================================
def structured_refine(base_prompt: str, system_prompt: str, schema: type[BaseModel]) -> BaseModel:
    """
    Refine a basic ad-lib prompt into a structured object using OpenAI's
    structured outputs. `schema` is the Pydantic model to parse into; the parsed
    instance (five components + a combined `final_prompt`) is returned.

    Exceptions are NOT caught here -- the caller (_safe_call in form_app) logs the
    full traceback and turns failures into a proper error response.
    """
    # Format the structured query (same message shape as the Groq refine call)
    completion = client.chat.completions.parse(
        # Request content
        messages=[
            {"role": "system", "content": system_prompt}, # System Prompt (text vs image)
            {"role": "user",   "content":   base_prompt}, # User message to respond to
        ],

        # The language model which will generate the completion
        model=STRUCTURED_MODEL,

        # Parse the reply straight into the Pydantic schema
        response_format=schema,
    )

    # Return the parsed Pydantic object (.parsed is an instance of `schema`)
    return completion.choices[0].message.parsed
