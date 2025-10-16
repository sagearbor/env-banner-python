# envbanner/adapters.py
import os
from .core import classify_env, build_banner_html

def dash(app, env_var_name: str = "APP_ENV"):
    """Patches Dash's index_string to include the banner."""
    env_var = os.getenv(env_var_name) or os.getenv("ENVBANNER_ENV")
    # For Dash, we don't know host at startup, so classify based on env var only.
    # The 'auto' mode will show a default 'dev' banner.
    env = classify_env(env_var=env_var, host=None, path=None)
    
    snippet = build_banner_html(env, host=None) # Host will be blank
    
    # Inject snippet before </body>
    original_index_string = app.index_string
    needle = "</body>"
    if needle in original_index_string.lower():
        parts = original_index_string.rsplit(needle, 1)
        app.index_string = parts[0] + snippet + needle + parts[1]
    else:
        app.index_string = original_index_string + snippet

def flask(app, env_var_name: str = "APP_ENV"):
    """Wraps a Flask app's WSGI application with the banner middleware."""
    from .middleware import WSGIBannerMiddleware
    app.wsgi_app = WSGIBannerMiddleware(app.wsgi_app, env_var_name=env_var_name)
