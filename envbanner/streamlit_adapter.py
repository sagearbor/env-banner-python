# envbanner/streamlit_adapter.py
import os
from .core import classify_env, banner_palette, banner_label, is_prod

def streamlit(env_var_name: str = "APP_ENV"):
    """
    Renders a Streamlit-safe banner using st.markdown (HTML+CSS only).
    Place this call near the top of your Streamlit script.
    """
    try:
        import streamlit as st
    except ImportError:
        print("Warning: Streamlit is not installed. Banner will not be shown.")
        return

    # Streamlit can't easily access the browser URL from the server,
    # so we rely primarily on the environment variable.
    env_var = os.getenv(env_var_name) or os.getenv("ENVBANNER_ENV")
    env = classify_env(env_var=env_var, host=None, path=None)

    if is_prod(env):
        return

    bg, fg = banner_palette(env)
    label = banner_label(env)

    # Note: Streamlit injects its own CSS which can be complex.
    # Using `position: fixed` is more reliable than `sticky` here.
    st.markdown(
        f"""
<div style="
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
  background: {bg};
  color: {fg};
  z-index: 999999;
  border-bottom: 1px solid rgba(0,0,0,.2);
">
  {label}
</div>
<style>
  /* Push down the main Streamlit content area */
  .main .block-container {{
    padding-top: 5rem;
  }}
</style>
""",
        unsafe_allow_html=True,
    )
