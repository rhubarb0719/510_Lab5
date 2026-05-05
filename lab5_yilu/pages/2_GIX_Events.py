"""Component E: events list + category filter."""

from __future__ import annotations

import sys
from pathlib import Path

_APP = Path(__file__).resolve().parent.parent
if str(_APP) not in sys.path:
    sys.path.insert(0, str(_APP))

import streamlit as st

from lib.supabase_app import get_supabase
from lib.ui import inject_accessible_theme

st.set_page_config(page_title="GIX Events", layout="wide")
inject_accessible_theme()
st.title("GIX Events")
st.caption("Reads `events` table; filter by category.")

sb = get_supabase()
if sb is None:
    st.warning("Set `SUPABASE_URL` and `SUPABASE_KEY` in `.env`.")
    st.stop()

categories = ["All"]
selected = "All"
rows = []

try:
    res = sb.table("events").select("*").order("starts_at").execute()
    rows = res.data or []
    # Component E: contract-style checks on Supabase → app pipeline
    assert isinstance(rows, list), "events query must return a list"
    assert all(isinstance(r, dict) for r in rows), "each event row must be a dict"
    cats = sorted({r.get("category") for r in rows if r.get("category")})
    categories = ["All"] + cats
except Exception as e:
    st.error(f"Could not load events (handled): {e}")
    st.stop()

selected = st.selectbox("Category", categories)

filtered = rows if selected == "All" else [r for r in rows if r.get("category") == selected]

if not filtered:
    st.info("No events for this filter. Insert sample rows in Supabase Table Editor.")
else:
    for ev in filtered:
        with st.container():
            st.markdown(f"### {ev.get('title', '(no title)')}")
            c1, c2, c3 = st.columns(3)
            c1.write(f"**Starts:** {ev.get('starts_at')}")
            c2.write(f"**Category:** {ev.get('category')}")
            c3.write(f"**Where:** {ev.get('location') or '—'}")
            if ev.get("description"):
                st.write(ev.get("description"))
            st.divider()
