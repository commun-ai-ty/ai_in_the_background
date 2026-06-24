"""
Helper code for querying the APIs & for refining prompts.
--------------------------------------------------------------------------------
`website.prompting`

"""
from groq import Groq

# Internal app code
from website.config import SYSTEM_PROMPT_TEXT

# Re-usable client -- TODO: Maybe the key goes here?
client = Groq()


# ================================================================================
# Stage 1: Prompt Refinement (simulating the "thinking" stage)
# ================================================================================
def refine_prompt(base_prompt: str, system_prompt: str = SYSTEM_PROMPT_TEXT) -> str:
     # Format the LLM query
    chat_completion = client.chat.completions.create(
        # Request content
        messages=[
            {"role": "system", "content": system_prompt}, # System Prompt (text vs image)
            {"role": "user",   "content":   base_prompt}, # User message to respond to
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
# TODO: Currently does not work -- no image generation model API available
def generate_ai_image(base_prompt: str) -> str:
    # Format the LLM query
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Write me a one paragraph short story based on this prompt."},
            {"role": "user",   "content": base_prompt}, # User message to respond to
        ],

        # The language model which will generate the completion
        model="llama-3.3-70b-versatile",

        # Max tokens (length) of the response
        max_completion_tokens=512,
    )

    # Get the response and return it
    response = chat_completion.choices[0].message.content
    return response


# --------------------------------------------------------------------------------
# Stage 2b: Generate short story
# --------------------------------------------------------------------------------
def generate_short_story(base_prompt: str) -> str:
    # Format the LLM query
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Write me a one paragraph short story based on this prompt."},
            {"role": "user",   "content": base_prompt}, # User message to respond to
        ],

        # The language model which will generate the completion
        model="llama-3.3-70b-versatile",

        # Max tokens (length) of the response
        max_completion_tokens=512,
    )

    # Get the response and return it
    response = chat_completion.choices[0].message.content
    return response


