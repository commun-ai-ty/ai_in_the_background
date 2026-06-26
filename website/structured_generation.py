"""
Structured generation for the chat prompt refinement.
--------------------------------------------------------------------------------
`website.structured_generation`

"""
import os, re

from openai   import OpenAI
from pydantic import Field, create_model

# Using the OpenAI library, but pointed at Groq's OpenAI-compatible endpoint + key,
# so structured generation runs on our Groq key.
client = OpenAI(
    base_url = "https://api.groq.com/openai/v1",
    api_key  = os.environ.get("GROQ_API_KEY"),
)

# Must be a Groq model that supports JSON-schema structured outputs
# Supported list: https://console.groq.com/docs/structured-outputs#supported-models
STRUCTURED_MODEL = "openai/gpt-oss-20b" # "meta-llama/llama-4-scout-17b-16e-instruct" | "moonshotai/kimi-k2-instruct"


# ================================================================================
# Build a Pydantic schema from editable field data ({title, description})
# ================================================================================
def _field_name(title: str, index: int) -> str:
    """Turn a human title into a safe Python identifier (fallback: field_{index})."""
    slug = re.sub(r"[^a-z0-9]+", "_", title.strip().lower()).strip("_")
    return slug or f"field_{index}"


def build_schema(fields: list[dict]):
    """
    Build a Pydantic model from a list of {title, description} dicts, plus an
    always-present `final_message`. Returns (model, names) where `names` holds the
    identifiers parallel to `fields` (so values can be mapped back to titles).
    """
    model_fields = {}
    names        = []
    used         = set()

    for i, f in enumerate(fields):
        name = _field_name(f.get("title", ""), i)
        # de-duplicate identifiers (two titles could slug to the same name)
        base, n = name, 2
        while name in used:
            name = f"{base}_{n}"
            n += 1
        used.add(name)
        names.append(name)
        model_fields[name] = (str, Field(description=f.get("description", "")))

    model_fields["final_message"] = (
        str,
        Field(description="The complete refined prompt as one ready-to-use string, building on all the steps above."),
    )
    return create_model("CustomRefinedPrompt", **model_fields), names


# ================================================================================
# Structured prompt refinement (OpenAI library -> Groq + Pydantic)
# ================================================================================
def structured_refine(base_prompt: str, system_prompt: str, fields: list[dict]) -> dict:
    """
    Refine a basic ad-lib prompt into a structured result using structured
    outputs. The schema is built from `fields` ({title, description}); returns
    {"components": [{title, description, value}], "final_message": str}.

    Exceptions are NOT caught here -- the caller (_safe_call in form_app) logs the
    full traceback and turns failures into a proper error response.
    """
    schema, names = build_schema(fields)

    # Manual override option for a demo
    use_prompt = base_prompt
    # "Draw a picture of an atom"

    # Format the structured query (same message shape as the Groq refine call)
    completion = client.chat.completions.parse(
        # Request content
        messages=[
            {"role": "system", "content": system_prompt}, # System Prompt (text vs image)
            {"role": "user",   "content":   use_prompt}, # User message to respond to
        ],

        # The language model which will generate the completion
        model=STRUCTURED_MODEL,

        # Parse the reply straight into the dynamically-built schema
        response_format=schema,
    )

    # Map the parsed values back onto the user-facing field titles
    parsed = completion.choices[0].message.parsed.model_dump()
    components = [
        {"title": f["title"], "description": f.get("description", ""), "value": parsed.get(name, "")}
        for f, name in zip(fields, names)
    ]

    return {"components": components, "final_message": parsed.get("final_message", "")}

