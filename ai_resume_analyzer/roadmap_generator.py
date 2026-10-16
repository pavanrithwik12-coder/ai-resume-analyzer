"""Module 6 and 7: rule-based learning roadmap and downloadable text report."""

LEARNING_TOPICS = {
    "python": "Python fundamentals, functions, OOP and virtual environments",
    "sql": "SQL joins, aggregations, subqueries and window functions",
    "excel": "Excel formulas, pivot tables and charts",
    "pandas": "Pandas: cleaning, grouping, merging and reshaping data",
    "numpy": "NumPy arrays and vectorised operations",
    "power bi": "Power BI: build an interactive dashboard from a dataset",
    "statistics": "Descriptive statistics, probability and hypothesis testing",
    "data visualization": "Data visualization with Matplotlib, Seaborn or Plotly",
    "matplotlib": "Matplotlib plots and chart styling",
    "machine learning": "Supervised and unsupervised learning, model evaluation",
    "scikit-learn": "scikit-learn pipelines, train/test split and cross-validation",
    "deep learning": "Neural networks, backpropagation and training with PyTorch or TensorFlow",
    "tensorflow": "TensorFlow / Keras: build and train a small model",
    "pytorch": "PyTorch tensors, datasets and training loops",
    "fastapi": "FastAPI basics: build and test a REST API",
    "flask": "Flask basics: routes, templates and a small web app",
    "django": "Django basics: models, views and the admin panel",
    "rest api": "REST API design: methods, status codes and JSON",
    "docker": "Docker fundamentals: images, containers and Dockerfiles",
    "git": "Git workflow: commits, branches and pull requests",
    "github": "GitHub: publish a repository with a good README",
    "mlflow": "MLflow experiment tracking and model registry",
    "nlp": "NLP basics: tokenisation, TF-IDF, embeddings and text classification",
    "spacy": "spaCy pipelines, NER and phrase matching",
    "nltk": "NLTK text preprocessing and basic analysis",
    "transformers": "Transformer models and fine-tuning with Hugging Face",
    "hugging face": "Hugging Face pipelines, datasets and model hub",
    "llm": "LLM basics: prompting, APIs and evaluation",
    "rag": "Retrieval-Augmented Generation: embeddings, vector search and a RAG demo",
    "langchain": "LangChain chains, tools and retrievers",
    "prompt engineering": "Prompt engineering patterns and controlled prompts",
    "opencv": "OpenCV image reading, filtering and feature detection",
    "cnn": "Convolutional neural networks for image classification",
    "yolo": "YOLO object detection: train and run a detector",
    "image processing": "Image processing: filters, thresholding and transformations",
}


def topic_for(skill: str) -> str:
    return LEARNING_TOPICS.get(skill, f"Learn the basics of {skill} and use it in a small project")


def generate_roadmap(missing, weak=None, per_week: int = 2):
    """Return a list of (week_label, text). Missing skills first, then a mini-project week."""
    weak = weak or []
    plan, week = [], 1
    for i in range(0, len(missing), per_week):
        chunk = missing[i:i + per_week]
        plan.append((f"Week {week}", "; ".join(topic_for(s) for s in chunk)))
        week += 1
    if weak:
        plan.append((f"Week {week}", "Strengthen with practice projects: " + ", ".join(weak)))
        week += 1
    if missing or weak:
        plan.append((f"Week {week}", "Build one small project that uses " + ", ".join((missing + weak)[:4]) + " and add it to your resume"))
    return plan


def build_report(target_role, ranking, found_by_category, gap, roadmap) -> str:
    top3 = ranking.head(3)
    target_row = ranking[ranking["Role"] == target_role].iloc[0]
    lines = ["AI RESUME ANALYSIS REPORT", "=" * 26, "",
             f"Target role: {target_role}",
             f"Resume match score: {target_row['Score']}%", "",
             "Skills found:"]
    for cat, skills in found_by_category.items():
        lines.append(f"  {cat}: {', '.join(skills)}")
    lines += ["", "Missing skills: " + (", ".join(gap["missing"]) or "none"),
              "Weak skills (mentioned once): " + (", ".join(gap["weak"]) or "none"), "",
              "Recommended roles:"]
    for i, r in enumerate(top3.itertuples(), 1):
        lines.append(f"  {i}. {r.Role} - {r.Score}%")
    lines += ["", "Suggested roadmap:"]
    lines += [f"  {w}: {t}" for w, t in roadmap]
    lines += ["", "NOTE: Match scores are estimates for learning guidance, not recruiter decisions.",
              "Missing keywords do not always mean missing ability."]
    return "\n".join(lines)
