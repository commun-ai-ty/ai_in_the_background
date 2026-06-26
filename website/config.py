"""
Configurable constants for the app.
--------------------------------------------------------------------------------
`website.config`

"""

# ================================================================================
# Ad-lib dropdown options  (edit these lists to change the dropdown choices)
# ================================================================================
ADLIB_OPTIONS = {
    "characters": [
        "Harry Potter",
        "Bluey",
        "Sherlock Holmes",
        "Mario",
        "Wonder Woman",
        "Spider-Man",
        "Dory",
        "Elsa",
        "K-Pop Demon Hunters",
        "a bunny",
    ],
    "styles": [
        "Balenciaga",
        "a Mystery Novel",
        "Medieval",
        "Cyberpunk",
        "SpongeBob",
        "the Wild West",
    ],
    "settings": [
        "a haunted castle",
        "a futuristic city",
        "the deep ocean",
        "a quiet village",
        "University of Michigan",
        "a fantastical forest",
        "a mystical savannah",
        "space",
    ],
}

# ================================================================================
# Image Mode (NOTE: Limited options due to it being "faked")
# ================================================================================
# We lock the dropdown options to the harry potter ones that the pre-made images
# were from.
IMAGE_MODE = {
    "character": "Harry Potter",
    "style": "Balenciaga",
    "setting": "a haunted castle",
    "basic_image": "basic_image.png",  # premade image for the BASIC prompt
    "refined_image": "refined_image.png",  # premade image for the REFINED prompt
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


# ================================================================================
# Structured-generation FIELD BANK
# ================================================================================
# Pre-defined steps users can DRAG into their refinement pipeline (per mode).
# The plan starts empty (only a `final_message` step, always appended by the
# schema builder); users compose their own order, e.g. Draft -> Critique -> final.
#
# "Draft"/"Critique" are generic reasoning steps shared by both modes.
_SHARED_STEPS = [
    {"title": "Draft",       "description": "Write a quick first-pass draft of the refined prompt."},
    {"title": "Critique",    "description": "Critique the draft above: what is weak, missing, or could be sharper? List concrete fixes."},
    {"title": "Brainstorm",  "description": "Brainstorm about what ideas we could cover in order to fully address the prompt."},
    {"title": "User Intent", "description": "Thinking about what the user's intent by asking this question is."},
]

FIELD_BANK = {

    # Image Generation
    "image": _SHARED_STEPS + [
        # What the picture is ABOUT (content / subject matter)
        {"title": "Core Subject",          "description": "The primary focus, described with precise, vivid physical details."},
        {"title": "Action & Moment",       "description": "What the subject is doing and the exact moment captured (e.g., mid-leap over a chasm, blowing out a candle, a tense standoff)."},
        {"title": "Mood & Emotion",        "description": "The feeling the image conveys through expression and body language (e.g., quiet wonder, looming dread, triumphant joy)."},
        {"title": "Story & Meaning",       "description": "The little story behind the picture: what is happening and why it matters (e.g., a daring rescue, a bittersweet goodbye)."},
        {"title": "Key Details & Symbols", "description": "Meaningful objects, clothing, or symbols that hint at the story (e.g., a cracked pocket watch, a royal crest, a single wilting rose)."},
        {"title": "Characters & Cast",     "description": "Who else appears and how they interact with the main character (e.g., a loyal sidekick, a sneering rival, a worried crowd)."},
        {"title": "Background & Setting",  "description": "What kinds of things might appear in the background, and what does the setting look like (e.g., the ground, skyline, buildings, etc.)?"},
        
        
        # How the picture is RENDERED (style & craft)
        {"title": "Medium & Style",        "description": "The specific visual format (e.g., 35mm macro photography, cyberpunk concept art, oil painting)."},
        {"title": "Lighting & Atmosphere", "description": "The mood and illumination (e.g., volumetric lighting, golden hour, bioluminescent glow)."},
        {"title": "Composition & Camera",  "description": "Framing and perspective (e.g., extreme close-up, low-angle shot, 24mm lens)."},
        {"title": "Quality & Technical",   "description": "Engine and render tags (e.g., 8k resolution, intricate details, masterpiece, octane render)."},
    ],

    # Short Story Generation
    "text": _SHARED_STEPS + [
        {"title": "Scene & Quote",             "description": "Reference a known scene or quote from the original story and work it in to the new story, but changed with our style twist added."},
        {"title": "Core Narrative Arc",        "description": "The immediate conflict, the climax, and the resolution/twist, compressed to fit one paragraph."},
        {"title": "Character & Perspective",   "description": "The focal character and the point of view (e.g., close third-person, unreliable first-person)."},
        {"title": "Setting & Sensory Anchors", "description": "The specific environment and 1-2 distinct sensory details (smell, sound, texture)."},
        {"title": "Tone & Voice",              "description": "The emotional atmosphere and stylistic execution (e.g., lyrical and melancholic, gritty realism)."},
        {"title": "Structural Constraints",    "description": "Instructions on pacing and structure (e.g., 'start in media res', 'end with a lingering question')."},
    ],
}

