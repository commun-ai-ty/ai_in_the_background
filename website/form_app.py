"""
Process user form inputs for the main app page.
--------------------------------------------------------------------------------
`website.form_app`

"""
import traceback
from flask import Blueprint, render_template, request, jsonify, url_for

# Internal app code
from website.prompting             import generate_ai_image, generate_short_story
from website.structured_generation import structured_refine
from website.config                import ADLIB_OPTIONS, IMAGE_MODE, STRUCTURED_FIELDS 
from website.config                import SYSTEM_PROMPT_IMAGE, SYSTEM_PROMPT_TEXT


# --------------------------------------------------------------------------------
# Create & route the Flask app
# --------------------------------------------------------------------------------
form_app = Blueprint("form_app", __name__)

@form_app.route("/test")
def test():
    # Hand the dropdown options + default structured-generation fields to the template
    return render_template("test.html", options=ADLIB_OPTIONS, structured_fields=STRUCTURED_FIELDS)


# ================================================================================
# Helpers
# ================================================================================
def _adlib_fields(data):
    """
    Pull + clean the three ad-lib selections from the request JSON.
    """
    return (
        (data.get("character") or "").strip(),
        (data.get("style"    ) or "").strip(),
        (data.get("setting"  ) or "").strip(),
    )

def _is_default_combo(character, style, setting):
    """
    True when the selections match the default combo (use the premade images).
    """
    return (
        character   == IMAGE_MODE["character"]
        and style   == IMAGE_MODE["style"    ]
        and setting == IMAGE_MODE["setting"  ]
    )

def _safe_call(fn, *args, label="operation"):
    """
    Run an external API call; on failure print the traceback to the server
    terminal and return (None, error_message) instead of raising.
    """
    try: return fn(*args), None
    except Exception as exc:
        print(f"\n[form_app] {label} FAILED:")
        traceback.print_exc()
        return None, str(exc)

def _clean_fields(raw, default):
    """
    Validate custom structured-generation fields posted from the page
    (a list of {title, description}); fall back to `default` if none are usable.
    Caps at 5 fields; a field needs at least a title.
    """
    if not isinstance(raw, list): return default

    cleaned = []
    for f in raw[:5]:                                  # cap at 5 fields
        if not isinstance(f, dict): continue
        title = (f.get("title"      ) or "").strip()
        desc  = (f.get("description") or "").strip()
        if title: cleaned.append({"title": title, "description": desc})

    return cleaned or default

# ================================================================================
# [TEXT MODE] One-shot: refine the prompt + generate two short stories
# ================================================================================
@form_app.route("/save", methods=["POST"])
def save():
    # Read JSON from the browser: {"mode": "...", "character": "...", "style": "...", "setting": "..."}
    data = request.get_json(silent=True) or {}
    character, style, setting = _adlib_fields(data)

    # Guard for missing selections
    if not character or not style or not setting:
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    # Construct the prompt from the ad-lib
    prompt_text = f" {character} {style} {setting}"

    # Refine with structured generation (fields come from the page, or the text defaults)
    fields = _clean_fields(data.get("fields"), STRUCTURED_FIELDS["text"])
    result, err = _safe_call(structured_refine, prompt_text, SYSTEM_PROMPT_TEXT, fields, label="prompt refinement")
    if err: return jsonify({"ok": False, "error": f"Refinement failed: {err}"}), 502
    refined_prompt = result["final_prompt"]

    # Generate a short story for each prompt
    basic_story   = generate_short_story(prompt_text)     # Top-right    -> uses the basic prompt
    refined_story = generate_short_story(refined_prompt)  # Bottom-right -> uses the refined prompt

    return jsonify({
        "ok"            : True,
        "mode"          : "text",
        "prompt_text"   : refined_prompt,
        "structured"    : result,          # {components, final_prompt} for the modal
        "basic_story"   : basic_story,
        "refined_story" : refined_story,
    })


# ================================================================================
# [IMAGE MODE] Staged generation -- the page calls these 3 routes in order
# ================================================================================
# NOTE: The default combo returns the premade /static images instead of generating

# --------------------------------------------------------------------------------
# Stage 1: Image from the BASIC (ad-lib) prompt
# --------------------------------------------------------------------------------
@form_app.route("/generate-basic-image", methods=["POST"])
def generate_basic_image():
    data = request.get_json(silent=True) or {}
    character, style, setting = _adlib_fields(data)

    # Guard for all arguments
    if (not character) or (not style) or (not setting):
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    # Check if we should use the default image or new ones
    if _is_default_combo(character, style, setting):
        image = url_for("static", filename=IMAGE_MODE["basic_image"])   # premade sample

    # Generate the basic image
    else:
        prompt_text = f" {character} {style} {setting}"
        image, err = _safe_call(generate_ai_image, prompt_text, label="basic image generation")
        if err: return jsonify({"ok": False, "error": f"Image generation failed: {err}"}), 502

    return jsonify({"ok": True, "image": image})

# --------------------------------------------------------------------------------
# Stage 2: Refine the ad-lib prompt (for image generation)
# --------------------------------------------------------------------------------
@form_app.route("/refine-prompt", methods=["POST"])
def refine_prompt_stage():
    data = request.get_json(silent=True) or {}
    character, style, setting = _adlib_fields(data)

    if not character or not style or not setting:
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    prompt_text = f" {character} {style} {setting}"

    # Refine with structured generation (fields come from the page, or the image defaults)
    fields = _clean_fields(data.get("fields"), STRUCTURED_FIELDS["image"])
    result, err = _safe_call(structured_refine, prompt_text, SYSTEM_PROMPT_IMAGE, fields, label="prompt refinement")
    if err: return jsonify({"ok": False, "error": f"Refinement failed: {err}"}), 502

    return jsonify({
        "ok"             : True,
        "refined_prompt" : result["final_prompt"],
        "structured"     : result,         # {components, final_prompt} for the modal
    })

# --------------------------------------------------------------------------------
# Stage 3: Image from the REFINED prompt
# --------------------------------------------------------------------------------
@form_app.route("/generate-refined-image", methods=["POST"])
def generate_refined_image():
    data = request.get_json(silent=True) or {}
    character, style, setting = _adlib_fields(data)
    refined_prompt = (data.get("refined_prompt") or "").strip()

    if _is_default_combo(character, style, setting):
        image = url_for("static", filename=IMAGE_MODE["refined_image"])  # premade sample
    else:
        if not refined_prompt: return jsonify({"ok": False, "error": "Missing refined prompt"}), 400
        image, err = _safe_call(generate_ai_image, refined_prompt, label="refined image generation")
        if err: return jsonify({"ok": False, "error": f"Image generation failed: {err}"}), 502

    return jsonify({"ok": True, "image": image})

