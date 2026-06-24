"""
Configurable constants for the app.
--------------------------------------------------------------------------------
`website.config`

"""


# ================================================================================
# Ad-lib dropdown options  (edit these lists to change the dropdown choices)
# ================================================================================
ADLIB_OPTIONS = {
    "characters": ["Harry Potter", "Sherlock Holmes", "Mario", "Wonder Woman"],
    "styles":     ["Balenciaga", "Van Gogh", "Studio Ghibli", "Cyberpunk"],
    "settings":   ["a haunted castle", "a futuristic city", "the deep ocean", "a quiet village"],
}


# ================================================================================
# Image Mode (NOTE: Limited options due to it being "faked")
# ================================================================================
# We lock the dropdown options to the harry potter ones that the pre-made images
# were from.
IMAGE_MODE = {
    "character":     "Harry Potter",
    "style":         "Balenciaga",
    "setting":       "a haunted castle",
    "basic_image":   "basic_image.png",     # premade image for the BASIC prompt
    "refined_image": "refined_image.png",   # premade image for the REFINED prompt
}



# --------------------------------------------------------------------------------
# System prompts (for text and for video)
# --------------------------------------------------------------------------------
# Image generation version
SYSTEM_PROMPT_IMAGE = """
Act as an expert AI image generation prompt engineer. 
Your goal is to take my basic concepts and transform them into highly detailed, 
optimized prompts suitable for advanced diffusion models and image generators 
(like Midjourney, Stable Diffusion, or DALL-E 3).\n\n

When I provide a basic idea, output a refined, comma-separated prompt that explicitly 
defines the following elements:\n

**Core Subject:** The primary focus, described with precise, vivid physical details.\n

**Medium & Style:** The specific visual format (e.g., 35mm macro photography, cyberpunk 
concept art, hyperrealistic oil painting).\n

**Lighting & Atmosphere:** The mood and illumination (e.g., volumetric lighting, 
inematic rim light, golden hour, bioluminescent glow).\n

**Composition & Camera:** Framing and perspective (e.g., extreme close-up, 
low-angle shot, 24mm lens, isometric perspective).\n

**Quality & Technical Specifiers:** Engine and render tags (e.g., 8k resolution, 
intricate details, masterpiece, octane render).\n

""".strip()

# Short story generation version
SYSTEM_PROMPT_TEXT = """
Act as an expert creative writing coach and prompt engineer. 
Your goal is to take my basic story idea and transform it into a highly 
detailed, optimized prompt designed to generate a compelling, perfectly 
paced one-paragraph short story.\n\n

When I provide a basic idea, output a comprehensive narrative prompt that 
explicitly defines the following elements for the AI writer:\n

**Core Narrative Arc:** The immediate conflict, the climax, and the 
resolution/twist, all compressed to fit naturally within a single paragraph.\n

**Character & Perspective:** The focal character and the point of view (e.g., 
close third-person, unreliable first-person).\n

**Setting & Sensory Anchors:** The specific environment and 1-2 distinct sensory 
details (smell, sound, texture) to quickly ground the reader.\n

**Tone & Voice:** The emotional atmosphere and stylistic execution (e.g., 
lyrical and melancholic, gritty realism, deadpan humor).\n

**Structural Constraints:** Specific instructions on pacing and structure 
(e.g., "Start in media res," "End with a lingering question," "Vary sentence 
lengths to build tension").\n

""".strip()






