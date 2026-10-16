"""Module 2: text cleaning. Keeps C++, C#, .NET style symbols and removes personal info."""
import re

# Lines that carry protected / personal attributes are dropped before any scoring.
PERSONAL_LINE = re.compile(
    r"\b(date of birth|dob|gender|sex|marital status|religion|nationality|age|passport)\b\s*[:\-]",
    re.IGNORECASE,
)


def remove_personal_info(text: str) -> str:
    """Remove emails, URLs, phone numbers and lines with protected attributes."""
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", " ", text)              # emails
    text = re.sub(r"(https?://\S+|www\.\S+)", " ", text)               # urls
    text = re.sub(r"(?:\+?\d[\s\-()]*){10,}", " ", text)               # phone numbers
    lines = [ln for ln in text.splitlines() if not PERSONAL_LINE.search(ln)]
    return "\n".join(lines)


def clean_text(text: str) -> str:
    """Lowercase, drop personal info, remove odd symbols and repeated spaces."""
    text = remove_personal_info(text).lower()
    text = re.sub(r"[\u2022\u25cf\u25aa\u25e6\u2023\u2219\u00b7]", " ", text)  # bullet symbols
    text = re.sub(r"[^a-z0-9+#./\-\n ]", " ", text)                    # keep + # . / - for C++, C#, .NET
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*", "\n", text)
    return text.strip()
