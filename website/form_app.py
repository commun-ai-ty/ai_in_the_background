"""
Process user form inputs for the main app page.
--------------------------------------------------------------------------------
`website.form_app`

"""
from flask        import Blueprint, render_template, request, jsonify, url_for

# Internal app code
from website.prompting import refine_prompt, generate_ai_image, generate_short_story
from website.config    import ADLIB_OPTIONS, IMAGE_MODE, SYSTEM_PROMPT_IMAGE, SYSTEM_PROMPT_TEXT

# --------------------------------------------------------------------------------
# Create & route the Flask app
# --------------------------------------------------------------------------------
form_app = Blueprint("form_app", __name__)

@form_app.route("/test")
def test():
    # Hand the dropdown options + image-mode combo to the template
    return render_template("test.html", options=ADLIB_OPTIONS, image_mode=IMAGE_MODE)


# ================================================================================
# Submitting custom prompts
# ================================================================================
@form_app.route("/save", methods=["POST"])
def save():
    # Read JSON from the browser -- {"mode": "...", "character": "...", "style": "...", "setting": "..."}
    data = request.get_json(silent=True) or {}
    mode      = (data.get("mode"     ) or "text").strip()
    character = (data.get("character") or ""    ).strip()
    style     = (data.get("style"    ) or ""    ).strip()
    setting   = (data.get("setting"  ) or ""    ).strip()

    # Guard for missing selections
    if not character or not style or not setting:
        return jsonify({"ok": False, "error": "Please choose all options"}), 400

    # Construct the prompt from the ad-lib
    prompt_text = f" {character} {style} {setting}"

    # --------------------------------------------------------------------------------
    # [IMAGE MODE] Refine the "prompt" (filled in ad-lib) for image generation
    # --------------------------------------------------------------------------------
    # NOTE: Not yet functional without an API key
    if mode == "image":
        refined_prompt = refine_prompt(prompt_text, system_prompt=SYSTEM_PROMPT_IMAGE)

        # TODO: Instead of actually generating two images, we just load two pre-made ones for now
        # ...
        # ...

        # Return content to the page
        return jsonify({
            "ok"            : True,
            "mode"          : "image",
            "prompt_text"   : refined_prompt,
            "basic_image"   : url_for("static", filename=IMAGE_MODE[  "basic_image"]),
            "refined_image" : url_for("static", filename=IMAGE_MODE["refined_image"]),
        })
    
    # --------------------------------------------------------------------------------
    # [TEXT MODE] Refine the "prompt" (filled in ad-lib) for image generation
    # --------------------------------------------------------------------------------
    elif mode == "text":
        refined_prompt = refine_prompt(prompt_text, system_prompt=SYSTEM_PROMPT_TEXT)

        # Generate a short story for each prompt
        basic_story   = generate_short_story(prompt_text)     # First row (top-right)  uses the basic prompt
        refined_story = generate_short_story(refined_prompt)  # Second row (bottom-right) uses the AI-refined prompt

        # Return content to the page
        return jsonify({
            "ok"            : True,
            "mode"          : "text",
            "prompt_text"   : refined_prompt,
            "basic_story"   : basic_story,
            "refined_story" : refined_story,
        })

