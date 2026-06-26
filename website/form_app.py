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
from website.config                import ADLIB_OPTIONS, IMAGE_MODE, FIELD_BANK
from website.config                import SYSTEM_PROMPT_IMAGE, SYSTEM_PROMPT_TEXT


# --------------------------------------------------------------------------------
# Create & route the Flask app
# --------------------------------------------------------------------------------
form_app = Blueprint("form_app", __name__)

@form_app.route("/test")
def test():
    # Hand the dropdown options + the structured-generation field bank to the template
    return render_template("test.html", options=ADLIB_OPTIONS, field_bank=FIELD_BANK)


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

def _clean_fields(raw):
    """
    Validate the structured-generation pipeline posted from the page (an ordered
    list of {title, description}). Returns the cleaned list -- possibly empty,
    since an empty plan just produces `final_message`. Caps at 6 steps.
    """
    if not isinstance(raw, list): return []

    cleaned = []
    for f in raw[:6]:                                  # cap at 6 steps
        if not isinstance(f, dict): continue
        title = (f.get("title"      ) or "").strip()
        desc  = (f.get("description") or "").strip()
        if title: cleaned.append({"title": title, "description": desc})

    return cleaned

# The page drives a 2-stage flow (both modes):
#   STAGE 1  -> basic result from the ad-lib prompt        (box 2)
#   STAGE 2  -> refine the prompt (box 3) + refined result (box 4)
# NOTE: In image mode, the default combo returns the premade /static images.

# ================================================================================
# STAGE 1: basic result from the ad-lib prompt (one route per mode)
# ================================================================================

# --------------------------------------------------------------------------------
# [TEXT] Basic short story from the ad-lib prompt
# --------------------------------------------------------------------------------
@form_app.route("/generate-basic-story", methods=["POST"])
def generate_basic_story():
    data = request.get_json(silent=True) or {}
    character, style, setting = _adlib_fields(data)

    if not character or not style or not setting:
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    prompt_text = f" {character} {style} {setting}"
    story, err = _safe_call(generate_short_story, prompt_text, label="basic story generation")
    if err: return jsonify({"ok": False, "error": f"Story generation failed: {err}"}), 502

    return jsonify({"ok": True, "story": story})

# --------------------------------------------------------------------------------
# [IMAGE] Basic image from the ad-lib prompt
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

# ================================================================================
# STAGE 2a: refine the ad-lib prompt (mode-aware structured generation)
# ================================================================================
@form_app.route("/refine-prompt", methods=["POST"])
def refine_prompt_stage():
    data = request.get_json(silent=True) or {}
    mode  = (data.get("mode") or "text").strip()
    character, style, setting = _adlib_fields(data)

    if not character or not style or not setting:
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    prompt_text = f" {character} {style} {setting}"

    # Mode only picks the system prompt now; the ordered pipeline comes from the page
    system_prompt = SYSTEM_PROMPT_IMAGE if mode == "image" else SYSTEM_PROMPT_TEXT

    fields = _clean_fields(data.get("fields"))
    result, err = _safe_call(structured_refine, prompt_text, system_prompt, fields, label="prompt refinement")
    if err: return jsonify({"ok": False, "error": f"Refinement failed: {err}"}), 502

    return jsonify({
        "ok"             : True,
        "refined_prompt" : result["final_message"],
        "structured"     : result,         # {components, final_message} for the page pipeline
    })


# ================================================================================
# STAGE 2b: refined result from the refined prompt (one route per mode)
# ================================================================================

# --------------------------------------------------------------------------------
# [TEXT] Refined short story from the refined prompt
# --------------------------------------------------------------------------------
@form_app.route("/generate-refined-story", methods=["POST"])
def generate_refined_story():
    data = request.get_json(silent=True) or {}
    refined_prompt = (data.get("refined_prompt") or "").strip()

    if not refined_prompt:
        return jsonify({"ok": False, "error": "Missing refined prompt"}), 400

    story, err = _safe_call(generate_short_story, refined_prompt, label="refined story generation")
    if err: return jsonify({"ok": False, "error": f"Story generation failed: {err}"}), 502

    return jsonify({"ok": True, "story": story})

# --------------------------------------------------------------------------------
# [IMAGE] Refined image from the refined prompt
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

