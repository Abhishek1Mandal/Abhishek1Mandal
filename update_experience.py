#!/usr/bin/env python3
"""
Auto-updates experience duration in README.md.
Designed to run via GitHub Actions on the 1st of every month.
"""

import re
from datetime import date

# Set this to the first day of your actual professional employment.
START_DATE = date(2023, 12, 1)
README_PATH = "README.md"


def calc_experience(start: date, today: date) -> str:
    """Return a clear duration such as '2 years 10 months'."""
    total_months = max(0, (today.year - start.year) * 12 + today.month - start.month)
    years, months = divmod(total_months, 12)
    year_label = "year" if years == 1 else "years"
    month_label = "month" if months == 1 else "months"
    return f"{years} {year_label} {months} {month_label}"


def update_readme(path: str, label: str) -> bool:
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    patterns = [
        (r'(<span id="experience-years">)[^<]*(</span>)', rf"\g<1>{label}\2"),
        (r'(<span id="about-experience">)[^<]*(</span>)', rf"\g<1>{label}\2"),
    ]

    updated = content
    for pattern, replacement in patterns:
        updated = re.sub(pattern, replacement, updated)

    if updated != content:
        with open(path, "w", encoding="utf-8") as file:
            file.write(updated)
        print(f"README updated: experience set to '{label}'")
        return True

    print(f"No changes needed (experience already '{label}' or spans not found)")
    return False


if __name__ == "__main__":
    today = date.today()
    label = calc_experience(START_DATE, today)
    print(f"Today: {today} | Start: {START_DATE} | Experience: {label}")
    update_readme(README_PATH, label)
