"""Shared Supabase client for Streamlit pages."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client

# Always load lab5_yilu/.env (not only cwd — Streamlit cwd can vary).
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")


def _env(name: str) -> Optional[str]:
    val = os.getenv(name)
    if val:
        return val
    try:
        import streamlit as st

        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return None


def get_supabase() -> Optional[Client]:
    url = _env("SUPABASE_URL")
    key = _env("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)
