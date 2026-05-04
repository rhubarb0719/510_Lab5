"""Shared Streamlit tweaks: readability + larger tap targets (mobile / accessibility)."""

from __future__ import annotations

import streamlit as st


def inject_accessible_theme() -> None:
    st.markdown(
        """
<style>
  /* Base text: larger + darker (Streamlit default gray is low-contrast) */
  .stApp, .stApp p, .stApp label, .stApp li {
    font-size: 1.05rem !important;
    color: #141414 !important;
  }
  [data-testid="stCaption"], div[data-testid="stCaption"] {
    color: #2d2d2d !important;
    font-size: 1rem !important;
  }
  .stMarkdown, .stMarkdown p {
    color: #141414 !important;
  }
  /* Form field labels */
  .stTextInput label, .stTextArea label, .stSelectbox label {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #141414 !important;
  }
  /* Buttons: bigger tap area + clearer text */
  .stButton > button {
    min-height: 3rem !important;
    padding: 0.65rem 1.35rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 0.5rem !important;
  }
  /* Dataframe / table text */
  [data-testid="stDataFrame"] {
    font-size: 1rem !important;
  }
  [data-testid="stDataFrame"] * {
    color: #141414 !important;
  }
  /* Sidebar */
  section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
    font-size: 1rem !important;
    color: #141414 !important;
  }
</style>
        """,
        unsafe_allow_html=True,
    )
