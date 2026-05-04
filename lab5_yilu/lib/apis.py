"""External REST calls + lightweight contract checks for Component B/D."""

from __future__ import annotations

from typing import Optional

import requests


def fetch_open_meteo_current(latitude: float, longitude: float) -> dict:
    """Open-Meteo: no API key. Used for happy-path / contract-style asserts."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    assert "current_weather" in data, "Open-Meteo JSON missing current_weather"
    cw = data["current_weather"]
    assert isinstance(cw, dict), "current_weather must be an object"
    assert "temperature" in cw, "current_weather missing temperature"
    assert isinstance(cw["temperature"], (int, float)), "temperature must be numeric"
    return data


def fetch_openfoodfacts_product(barcode: str) -> Optional[dict]:
    """Free barcode lookup (food-heavy catalog). No API key. Returns None if not found."""
    code = "".join(c for c in barcode.strip() if c.isdigit())
    if not code:
        return None
    url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    assert isinstance(data, dict), "OpenFoodFacts root must be object"
    assert "status" in data, "OpenFoodFacts JSON missing status"
    if data.get("status") != 1:
        return None
    product = data.get("product") or {}
    assert isinstance(product, dict), "product must be object when status==1"
    return product
