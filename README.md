# commun-ai-ty web app template

This repository is a **starter template** for building small, self-contained web applications that can be **hosted and supported by the commun-ai-ty server**.

It is intentionally simple:

- A **Flask** application (with Jinja templates)
- A **Blueprint** for routes
- A single environment variable, **`URL_PREFIX`**, to make the app “mountable” under a subpath (how the commun-ai-ty server can host many apps on one domain)

## What’s in this repo

### High-level architecture

- **`main.py`**: local dev entrypoint. Creates the Flask app and runs it.
- **`website/`**: the Python package that defines the Flask app.
  - **`website/__init__.py`**: `create_app()` (the app factory). Reads `URL_PREFIX` and registers blueprints.
  - **`website/home_dash.py`**: a Flask `Blueprint` with the `/` homepage route.
  - **`website/templates/`**: Jinja templates (currently `home.html`).
- **`pyproject.toml`** + **`setup.py`**: packaging metadata and dependencies (installable via pip).

### How the pieces work together

1. `main.py` imports `create_app()` from `website`.
2. `website.create_app()` creates a Flask app and registers one or more blueprints.
3. The homepage route in `website/home_dash.py` renders `website/templates/home.html`.
4. If `URL_PREFIX` is set, both routing *and* static assets are served under that prefix, so the app works correctly behind a reverse proxy.

## Quickstart (local development)

From the `main/` directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
python main.py
```

Then open `http://localhost:8094/`.

## Running under a URL prefix (how production hosting works)

On the commun-ai-ty server, your app will typically be hosted under a subpath such as:

- `/apps/<your-app-slug>/`

To support that, this template uses an environment variable:

- **`URL_PREFIX`**: a path prefix such as `/apps/my-demo`

When `URL_PREFIX` is set:

- Flask routes are registered at `url_prefix=URL_PREFIX`
- Static files are served from `static_url_path=f"{URL_PREFIX}/static"`

You can simulate this locally:

```bash
export URL_PREFIX="/apps/demo"
python main.py
```

Now your app should be available at:

- `http://localhost:8094/apps/demo/`

### Important rules when using `URL_PREFIX`

- **Always generate URLs with `url_for(...)`** (as the template does). Avoid hard-coding links like `href="/something"` because they will break when the app is mounted under a prefix.
- **Serve static assets via `url_for('static', filename=...)`** so paths include the prefix automatically.

## Adding pages and features

### Add a new route (simple Flask page)

Edit `website/home_dash.py` and add a new route on the `home_dash` blueprint:

- Keep the route path **relative** (e.g. `"/about"`), because the prefix is applied when registering the blueprint.
- Render a new template in `website/templates/`.

### Add a new blueprint (recommended as your app grows)

1. Create `website/<feature>.py` with a `Blueprint`.
2. Import and `register_blueprint(...)` it inside `website/__init__.py`.

This keeps your app modular and makes it easier for commun-ai-ty maintainers to review and support.

## Static files (images, CSS, JS)

This template references images like:

- `{{ url_for('static', filename='commun-ai-ty_logo_color.png') }}`

To add your own assets:

1. Create a folder `website/static/`
2. Put assets inside (e.g. `website/static/logo.png`)
3. Reference them with `url_for('static', filename='logo.png')`

## Dash / Plotly (optional)

`pyproject.toml` includes `dash` and the template imports Plotly in `website/home_dash.py`.

You can build interactive visualizations in two common ways:

- **Plotly in templates**: generate a Plotly figure in Flask, serialize it to JSON, and render it in a Jinja template.
- **Dash embedded in Flask**: mount a Dash app onto the same Flask server (useful for heavier interactivity).

If you don’t plan to use Dash, you can remove `dash` from dependencies and delete unused imports.

## Installing dependencies

This project is a standard Python package. The recommended install is editable mode:

```bash
pip install -e .
```

Optional dev tools (formatting/linting/type-checking):

```bash
pip install -e ".[dev]"
```

## Deployment expectations (commun-ai-ty server)

This repo is designed so commun-ai-ty can host and support your app with minimal changes:

- **One Python web server** (Flask app) per app
- **Mountable under a subpath** via `URL_PREFIX`
- **No hard-coded domain/path assumptions**
- A clear separation between:
  - Python routing/business logic (`website/*.py`)
  - UI (`website/templates/` and `website/static/`)

If you add additional services (databases, background jobs, external APIs), document them here and ensure they work in the commun-ai-ty hosting environment.

## Troubleshooting

- **Page loads but CSS/images 404 in production**: you probably hard-coded `/static/...` instead of using `url_for('static', filename=...)`, or you’re not serving assets under `URL_PREFIX`.
- **Routes work locally but not when mounted**: you probably hard-coded links like `href="/about"` instead of using `url_for(...)`.
- **Nothing responds on `localhost:8094`**: ensure you’re running from `main/` and installed dependencies in an active virtualenv.