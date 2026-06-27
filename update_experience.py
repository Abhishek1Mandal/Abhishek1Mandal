#!/usr/bin/env python3
"""
Auto-updates experience years in README.md.
Runs via GitHub Actions on the 1st of every month at midnight.
"""

import re
from datetime import date

# ── CONFIG ────────────────────────────────────────────────────────────────────
START_DATE = date(2023, 7, 1)   # ← Set your career start date here (YYYY, M, D)
README_PATH = "README.md"
# ─────────────────────────────────────────────────────────────────────────────


def calc_experience(start: date, today: date) -> str:
    """
    Returns a precise monthly label like '3.6', '3.7', '4.0', etc.
    Format: whole_years.months_remainder — updates every month.
    e.g. 3 years 7 months → 3.7 | 4 years 0 months → 4.0
    """
    total_months = (today.year - start.year) * 12 + (today.month - start.month)
    whole_years = total_months // 12
    remaining_months = total_months % 12
    return f"{whole_years}.{remaining_months}"


def update_readme(path: str, label: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Targets both span ids used in the README
    patterns = [
        # <span id="experience-years">3.5</span>
        (r'(<span id="experience-years">)[\d.]+?(</span>)', rf'\g<1>{label}\2'),
        # <span id="about-experience">3.5</span>
        (r'(<span id="about-experience">)[\d.]+?(</span>)', rf'\g<1>{label}\2'),
        # Plain text fallbacks: "3.5 years" / "4.0 Years"
        (r'\b[\d.]+\s+([Yy]ears?\b)', rf'{label} \1'),
    ]

    updated = content
    changed = False
    for pattern, replacement in patterns:
        new = re.sub(pattern, replacement, updated)
        if new != updated:
            changed = True
        updated = new

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✅ README updated → experience set to '{label}'")
    else:
        print(f"ℹ️  No changes needed (already '{label}' or pattern not found)")

    return changed


if __name__ == "__main__":
    today = date.today()
    label = calc_experience(START_DATE, today)
    print(f"📅 Today: {today}  |  Start: {START_DATE}  |  Label: {label}")
    update_readme(README_PATH, label)