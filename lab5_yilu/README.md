# TECHIN 510 - Week 5: Full Stack Development

## Instructions

See lab-manual.md for full lab instructions. Submit deliverables on Github Classroom (main branch).

## Quick run (Streamlit — Component B + E skeleton)

1. Python 3.10+ recommended; create a venv and install deps:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. In Supabase SQL Editor, run `supabase/schema.sql`, then optional `supabase/seed_events.sql`.

3. Copy `.env.example` → `.env` and add `SUPABASE_URL` / `SUPABASE_KEY`. Disable RLS on `return_lines` and `events` if inserts fail.

4. From this folder (`lab5_yilu/`):

   ```bash
   cd lab5_yilu
   streamlit run Home.py
   ```

   - **Home** (`/`): return lines + Open-Meteo sidebar + optional Open Food Facts barcode lookup + CSV download stub.
   - **GIX Events**: multipage sidebar → category filter over `events`.