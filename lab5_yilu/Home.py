"""Component B: minimal Streamlit + Supabase + external APIs (Open-Meteo + optional Open Food Facts)."""

from __future__ import annotations

import io
import sys
from pathlib import Path

# Streamlit Cloud runs from repo root; ensure `lab5_yilu` is on sys.path.
_APP = Path(__file__).resolve().parent
if str(_APP) not in sys.path:
    sys.path.insert(0, str(_APP))

import pandas as pd
import streamlit as st

from lib.apis import fetch_open_meteo_current, fetch_openfoodfacts_product
from lib.supabase_app import get_supabase
from lib.text_clean import suggest_clean_name
from lib.ui import inject_accessible_theme

st.set_page_config(page_title="Week 5 Lab — Returns intake", layout="wide")
inject_accessible_theme()

st.title("Equipment return intake")
st.caption(
    "Stores rows in Supabase for CSV export; optional barcode lookup uses free Open Food Facts."
)


with st.sidebar:
    st.subheader("External API (Open-Meteo)")
    try:
        # Seattle-ish coords — satisfies external REST integration + asserts inside helper.
        wx = fetch_open_meteo_current(47.6588, -122.3135)
        temp = wx["current_weather"]["temperature"]
        st.metric("Current temp (Open-Meteo)", f"{temp} °C")
    except Exception as e:
        st.error(f"Weather fetch failed: {e}")

sb = get_supabase()
if sb is None:
    st.warning("Set `SUPABASE_URL` and `SUPABASE_KEY` in `.env` (see `.env.example`).")

with st.form("line"):
    amazon_title = st.text_area("Amazon / vendor title (long OK)")
    barcode = st.text_input("Optional barcode digits (Open Food Facts lookup)")
    asset_sid = st.text_input("Optional asset SID / tag")
    cleaned_default = suggest_clean_name(amazon_title)
    cleaned_name = st.text_input("Cleaned product name (BlueTally-friendly)", value=cleaned_default)

    submitted = st.form_submit_button("Save line to Supabase", type="primary", use_container_width=True)

if submitted:
    if not amazon_title.strip() or not cleaned_name.strip():
        st.error("Amazon title and cleaned name are required.")
    else:
        hint_used = False
        if barcode.strip():
            try:
                prod = fetch_openfoodfacts_product(barcode)
                if prod and prod.get("product_name"):
                    hint_used = True
                    st.success(f"Barcode lookup: “{prod.get('product_name')}”")
            except Exception as e:
                st.warning(f"Barcode lookup failed (handled): {e}")

        if sb is None:
            st.error("Supabase not configured.")
        else:
            try:
                sb.table("return_lines").insert(
                    {
                        "amazon_title": amazon_title.strip(),
                        "cleaned_name": cleaned_name.strip(),
                        "barcode": barcode.strip() or None,
                        "asset_sid": asset_sid.strip() or None,
                    }
                ).execute()
                st.success("Saved.")
                if hint_used:
                    st.info("If lookup matched food packaging, still verify name for AV gear.")
            except Exception as e:
                st.error(f"Database error (handled): {e}")

st.divider()
st.subheader("Saved rows → CSV (BlueTally-style columns)")
if sb is None:
    st.info("Connect Supabase to load rows.")
else:
    try:
        res = sb.table("return_lines").select("*").order("created_at", desc=True).limit(200).execute()
        rows = res.data or []
        if not rows:
            st.write("No rows yet.")
        else:
            df = pd.DataFrame(rows)
            display_cols = ["cleaned_name", "asset_sid", "status", "location", "amazon_title", "barcode"]
            existing = [c for c in display_cols if c in df.columns]
            st.dataframe(df[existing], use_container_width=True)

            export_df = pd.DataFrame(
                {
                    "product_name": df.get("cleaned_name", ""),
                    "asset_number": df.get("asset_sid", ""),
                    "status": df.get("status", ""),
                    "location": df.get("location", ""),
                }
            )
            buf = io.StringIO()
            export_df.to_csv(buf, index=False)
            st.download_button(
                "Download CSV",
                data=buf.getvalue(),
                file_name="bluetally_import_stub.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True,
            )
    except Exception as e:
        st.error(f"Load failed (handled): {e}")
