"""Module 4, 5 and 6: job-role dataset, TF-IDF + cosine matching, skill-gap analysis."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

W_COVERAGE = 0.7      # share of required skills found in the resume
W_SIMILARITY = 0.3    # TF-IDF cosine similarity between candidate skills and role skills


def load_roles(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["skills_list"] = df["required_skills"].apply(lambda s: [x.strip().lower() for x in s.split("|")])
    return df


def _skill_doc(skills) -> str:
    # one token per skill, e.g. "power bi" -> "power_bi"
    return " ".join(s.replace(" ", "_") for s in skills)


def match_roles(clean_text: str, found_skills, roles_df: pd.DataFrame) -> pd.DataFrame:
    """Score the resume against every role and return roles ranked high to low."""
    found = set(found_skills)

    # (a) TF-IDF vectors of candidate skills and role skills -> cosine similarity
    role_docs = roles_df["skills_list"].apply(_skill_doc).tolist()
    cand_doc = _skill_doc(sorted(found))
    vec = TfidfVectorizer(analyzer=str.split)
    matrix = vec.fit_transform(role_docs + [cand_doc])
    skill_sim = cosine_similarity(matrix[-1], matrix[:-1]).ravel()

    # (b) TF-IDF vectors of the full resume text and role descriptions (shown for reference)
    role_text = (roles_df["skills_list"].apply(" ".join) + " " + roles_df["description"].str.lower()).tolist()
    vec2 = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), token_pattern=r"[a-z0-9][a-z0-9+#.\-]*")
    matrix2 = vec2.fit_transform([clean_text] + role_text)
    text_sim = cosine_similarity(matrix2[0], matrix2[1:]).ravel()

    rows = []
    for i, role in roles_df.iterrows():
        required = role["skills_list"]
        matched = [s for s in required if s in found]
        missing = [s for s in required if s not in found]
        coverage = len(matched) / len(required)
        score = 100 * (W_COVERAGE * coverage + W_SIMILARITY * skill_sim[i])
        rows.append({
            "Role": role["role"],
            "Score": round(score, 1),
            "Skill coverage %": round(100 * coverage, 1),
            "Skill similarity %": round(100 * skill_sim[i], 1),
            "Text similarity %": round(100 * text_sim[i], 1),
            "Matched": matched,
            "Missing": missing,
        })
    return pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)


def skill_gap(found: dict, roles_df: pd.DataFrame, role_name: str) -> dict:
    """Skills present, weak (mentioned only once) and missing for one target role."""
    required = roles_df.loc[roles_df["role"] == role_name, "skills_list"].iloc[0]
    present = [s for s in required if s in found]
    weak = [s for s in present if found[s]["count"] == 1]
    missing = [s for s in required if s not in found]
    return {"required": required, "present": present, "weak": weak, "missing": missing}
