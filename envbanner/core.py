# envbanner/core.py
import os
import re
from html import escape
from typing import Optional, Tuple

# Map host/path to env buckets; override with ENVBANNER_MAP if needed.
DEFAULT_RULES = [
    # dev/local/test
    (r"(localhost|127\.0\.0\.1|\.local$)", "dev"),
    (r"(^|\.)dev(\.|-)|(\b)dev(\b)", "dev"),
    (r"(^|\.)test(\.|-)|(\b)qa(\b)|(\b)sandbox(\b)", "dev"),
    (r":\d{2,5}$", "dev"),  # non-standard port is a strong hint

    # staging/validation
    (r"(^|\.)stg(\.|-)|(^|\.)stage(\.|-)|(^|\.)staging(\.)", "staging"),
    (r"(^|\.)val(\.|-)|(\b)validation(\b)|(\b)preprod(\b)", "staging"),
]

ENV_NORMS = {
    "prod": "prod", "production": "prod",
    "staging": "staging", "stage": "staging", "stg": "staging",
    "val": "staging", "validation": "staging", "preprod": "staging",
    "dev": "dev", "development": "dev",
    "local": "dev",
    "test": "dev", "qa": "dev",
    "unknown": "unknown", "auto": "auto",
}

def _norm_env(value: Optional[str]) -> Optional[str]:
    if not value: return None
    v = value.strip().lower()
    return ENV_NORMS.get(v, v)

def classify_from_host_path(host: str, path: str) -> str:
    text = f"{host}{path}".lower()
    for pattern, env in DEFAULT_RULES:
        if re.search(pattern, text):
            return env
    return "unknown"

def classify_env(*, env_var: Optional[str], host: Optional[str], path: Optional[str]) -> str:
    # 1) Explicit env var wins if provided
    e = _norm_env(env_var)
    if e and e != "auto":
        return e

    # 2) Host/path detection when available
    if host:
        detected = classify_from_host_path(host, path or "")
        if detected != "unknown":
            return detected
        return "dev" # unknown from host: prefer safety unless explicitly prod

    # 3) Last resort
    return "dev"  # safe default

def is_prod(env: str) -> bool:
    return env == "prod"

def banner_palette(env: str) -> Tuple[str, str]:
    """Returns (bg, fg) hex colors by env bucket."""
    if env == "staging":
        return ("#f59e0b", "#111827")  # amber-500 bg, gray-900 text
    # dev/test/local/unknown -> red
    return ("#ef4444", "#ffffff")     # red-500 bg, white text

def banner_label(env: str) -> str:
    if env == "prod": return ""
    if env == "staging": return "STAGING"
    if env in ("dev", "test", "local"): return env.upper()
    if env == "unknown": return "NON-PROD (UNKNOWN)"
    return env.upper()

def build_banner_html(env: str, host: Optional[str]) -> str:
    """Returns a self-contained HTML+CSS snippet (inline)."""
    if is_prod(env): return ""

    bg, fg = banner_palette(env)
    label = banner_label(env)
    host_text = f" • {host}" if host else ""
    text = f"{escape(label)}{escape(host_text)}"

    # Using a CSS-only approach with a sibling element to push content down
    # is more robust and avoids JS for layout modification.
    return f"""
<style>
  #env-banner-bar {{
    position: fixed; top: 0; left: 0; right: 0; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-family: system-ui, sans-serif; font-size: 12px; font-weight: 700;
    z-index: 2147483647; background: {bg}; color: {fg};
    text-transform: uppercase; box-shadow: 0 1px 3px rgba(0,0,0,.2);
  }}
  /* Push down body content */
  body {{ padding-top: 32px !important; }}
</style>
<div id="env-banner-bar" role="status">{text}</div>
"""
