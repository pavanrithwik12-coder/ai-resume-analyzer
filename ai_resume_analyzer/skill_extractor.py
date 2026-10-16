"""Module 3: controlled-dictionary skill extraction, categories and simple section detection."""
import re
from collections import defaultdict

import pandas as pd


def load_skill_dictionary(path: str) -> pd.DataFrame:
    df = pd.read_csv(path).fillna("")
    df["alias_list"] = df.apply(
        lambda r: [r["skill"].lower()] + [a.strip().lower() for a in str(r["aliases"]).split("|") if a.strip()],
        axis=1,
    )
    return df


def _pattern(alias: str):
    # Whole-term match that still works for c++, c#, .net, scikit-learn
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])")


def extract_skills(clean_text: str, skill_df: pd.DataFrame) -> dict:
    """Return {skill: {"category": ..., "count": n}} for every dictionary skill found."""
    found = {}
    for _, row in skill_df.iterrows():
        count = sum(len(_pattern(alias).findall(clean_text)) for alias in row["alias_list"])
        if count > 0:
            found[row["skill"]] = {"category": row["category"], "count": count}
    return found


def group_by_category(found: dict) -> dict:
    grouped = defaultdict(list)
    for skill, info in found.items():
        grouped[info["category"]].append(skill)
    return {cat: sorted(skills) for cat, skills in sorted(grouped.items())}


SECTION_HEADINGS = {
    "education": {"education", "academic qualification", "academics"},
    "skills": {"skills", "technical skills", "key skills"},
    "projects": {"projects", "academic projects", "personal projects"},
    "experience": {"experience", "work experience", "internship", "internships"},
}


def detect_sections(clean_text: str) -> dict:
    """Split cleaned resume text into education / skills / projects / experience."""
    sections, current = {}, None
    for line in clean_text.splitlines():
        head = line.strip().strip(":")
        match = next((name for name, words in SECTION_HEADINGS.items() if head in words), None)
        if match:
            current = match
            sections.setdefault(current, [])
        elif current:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}
