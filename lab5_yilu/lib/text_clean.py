"""Very small Amazon-title cleanup — interview tie-in without paid APIs."""


def suggest_clean_name(amazon_title: str) -> str:
    t = (amazon_title or "").strip()
    if not t:
        return ""
    # Prefer first segment before common separators (cheap heuristic).
    for sep in [" — ", " - ", " | ", ","]:
        if sep in t:
            t = t.split(sep)[0].strip()
            break
    return t[:200]
