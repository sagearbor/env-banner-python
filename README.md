# Environment Banner (`env-banner`)

A single, portable Python utility to display an environment warning banner (e.g., "DEVELOPMENT", "STAGING") across any web framework. One source of truth, one-line usage per app.

## Why This Exists

In a complex development environment with multiple repositories and environments (dev, test, staging), it's easy to accidentally use a non-production system with production data. This utility prevents such mistakes by displaying a clear, unavoidable banner on all non-production deployments.

This library is designed to be:

* **Portable**: A single package that works in any Python web project.
* **Bulletproof**: Uses reliable server-side detection and sane defaults. It fails safe by showing a banner if the environment is unknown.
* **Thoughtless**: Requires only a one-line integration for most major frameworks.
* **Framework-Agnostic**: Works with FastAPI, Starlette, Flask, Django, Dash, and Streamlit out of the box.
* **Maintainable**: All banner logic, colors, and rules are in one place. Update it once, and all projects inherit the changes.

## Repository Structure

The repository is structured as a standard Python package. When integrating manually, you only need to copy the `envbanner/` directory into your project.

```
env-banner/
├── envbanner/
│   ├── __init__.py
│   ├── adapters.py
│   ├── core.py
│   ├── middleware.py
│   └── streamlit_adapter.py
├── LICENSE
├── pyproject.toml
└── README.md
```

## Installation

You can either copy the `envbanner/` directory directly into your project's shared utilities folder, or you can install it directly from a Git repository:

```bash
pip install "git+[https://github.com/your-username/env-banner.git#egg=env-banner](https://github.com/your-username/env-banner.git#egg=env-banner)"
```

## How It Works

The utility uses a middleware-first approach.

1.  **Environment Classification**: It determines the current environment by checking the `APP_ENV` environment variable first, then falling back to reliable server-side request details (host, path). It defaults to `dev` if uncertain.
2.  **Middleware Injection (WSGI/ASGI)**: For frameworks like Flask, FastAPI, and Django, it uses a middleware to automatically inject the banner HTML into any `text/html` response just before it's sent to the browser.
3.  **Adapters (Dash/Streamlit)**: For frameworks where middleware isn't a natural fit, it provides simple one-line adapter functions that patch the application or inject the banner using framework-specific methods.

## Configuration

The banner's behavior is controlled primarily by a single environment variable:

**`APP_ENV`** (or `ENVBANNER_ENV`)

Set this variable in your deployment environment (Docker, Kubernetes, etc.).

* `prod` or `production`: **No banner** is shown.
* `staging`, `val`, `preprod`: A **yellow banner** is shown.
* `dev`, `test`, `local`: A **red banner** is shown.
* **If unset**: A **red banner** is shown by default.

## Usage

Import the library and add the single integration line to your application.

### FastAPI / Starlette (ASGI)

```python
from fastapi import FastAPI
from envbanner import ASGIBannerMiddleware

app = FastAPI()
app.add_middleware(ASGIBannerMiddleware) # <-- Add this line
```

### Flask (WSGI)

```python
from flask import Flask
from envbanner import flask as envbanner_flask

app = Flask(__name__)
envbanner_flask(app) # <-- Add this line
```

### Django

In your `settings.py`, add the middleware to your `MIDDLEWARE` list. It should be placed early in the list.

```python
# settings.py
MIDDLEWARE = [
    'envbanner.middleware.WSGIBannerMiddleware', # <-- Add this line
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ...
]
```

### Dash

```python
import dash
from envbanner import dash as envbanner_dash

app = dash.Dash(__name__)
envbanner_dash(app) # <-- Add this line
```

### Streamlit

Place this line near the top of your Streamlit script.

```python
import streamlit as st
import envbanner

envbanner.streamlit() # <-- Add this line

st.title("My Streamlit App")
# ...
```
