-- Run in Supabase SQL Editor. Turn off RLS on these tables for lab (Table Editor -> shield icon).

-- Component B: equipment return lines → export CSV for BlueTally-style workflows
create table if not exists public.return_lines (
  id uuid primary key default gen_random_uuid(),
  amazon_title text not null,
  cleaned_name text not null,
  barcode text,
  asset_sid text,
  status text not null default 'pending_import',
  location text not null default 'GIX',
  created_at timestamptz not null default now()
);

-- Component E: GIX events (category filter in UI)
create table if not exists public.events (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  starts_at timestamptz not null,
  category text not null,
  location text,
  description text,
  created_at timestamptz not null default now()
);
