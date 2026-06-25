"""
Helper code for querying the APIs & for refining prompts.
--------------------------------------------------------------------------------
`website.prompting`

"""

from groq import Groq
from openai import OpenAI

# Internal app code
from website.config import SYSTEM_PROMPT_TEXT

# Re-usable client -- TODO: Maybe the key can go here?
client = Groq()
client_images = OpenAI()

# Give up on an image request after this many seconds (so it can't hang forever)
IMAGE_TIMEOUT = 240

# Image model to use
IMAGE_MODEL = "gpt-image-1"


# ================================================================================
# Stage 1: Prompt Refinement (simulating the "thinking" stage)
# ================================================================================
def refine_prompt(base_prompt: str, system_prompt: str = SYSTEM_PROMPT_TEXT) -> str:
    # Format the LLM query
    chat_completion = client.chat.completions.create(
        # Request content
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },  # System Prompt (text vs image)
            {"role": "user", "content": base_prompt},  # User message to respond to
        ],
        # The language model which will generate the completion
        model="llama-3.3-70b-versatile",
        # Max tokens (length) of the response
        max_completion_tokens=256,
    )

    # Get the response and return it
    response = chat_completion.choices[0].message.content
    return response


# --------------------------------------------------------------------------------
# Stage 2a: Generate image
# --------------------------------------------------------------------------------
def generate_ai_image(base_prompt: str) -> str:
    """
    Generate an image and return it as a base64 PNG data URI.

    Exceptions are NOT caught here -- the caller (_safe_call in form_app) logs
    the full traceback and turns failures into a proper error response, so the
    page can show the real reason instead of a broken image.
    """
    # gpt-image-* returns base64 by default (no response_format param)
    response = client_images.with_options(timeout=IMAGE_TIMEOUT).images.generate(
        model=IMAGE_MODEL,
        prompt=base_prompt,
        n=1,  # Number of images to generate
        size="1024x1024",
    )

    # response.data[0].b64_json is the base64-encoded PNG
    image_base64 = response.data[0].b64_json

    # Hand back a data URI the browser can drop straight into an <img src>
    return f"data:image/png;base64,{image_base64}"


# --------------------------------------------------------------------------------
# Stage 2b: Generate short story
# --------------------------------------------------------------------------------
def generate_short_story(base_prompt: str) -> str:
    # Format the LLM query
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Write me a one paragraph short story based on this prompt.",
            },
            {"role": "user", "content": base_prompt},  # User message to respond to
        ],
        # The language model which will generate the completion
        model="llama-3.3-70b-versatile",
        # Max tokens (length) of the response
        max_completion_tokens=512,
    )

    # Get the response and return it
    response = chat_completion.choices[0].message.content
    return response
