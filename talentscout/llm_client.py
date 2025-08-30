"""
LLM client wrapper. Uses Google Gemini if GOOGLE_API_KEY is present.
Provides a fallback question-generator if API not available or request fails.
"""

import os
import json
from typing import List, Dict

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_KEY) if GOOGLE_KEY and GEMINI_AVAILABLE else None

DEFAULT_MODEL = "gemini-1.5-flash"


def call_gemini_chat(system: str, user: str, model: str = DEFAULT_MODEL, temperature: float = 0.3) -> str:
    """
    Calls Gemini model and returns assistant content. Raises exceptions on failure.
    """
    if not client:
        raise RuntimeError("GOOGLE_API_KEY not set or google-genai not installed")

    prompt = f"{system}\n\n{user}"
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": temperature}
    )
    return resp.text.strip()


# ---------- Fallback simple generator ----------
def fallback_generate_questions(tech: str, count: int = 4) -> List[str]:
    """
    Heuristic question generator when no LLM is reachable.
    Produces a variety of conceptual, practical, debugging and advanced questions.
    """
    tech_lower = tech.lower()
    questions = []
    if "python" in tech_lower:
        templates = [
            "Explain how Python's GIL affects multi-threaded programs. Give an example.",
            "How would you profile a slow Python function and optimize it?",
            "Write a function to remove duplicates from a list while preserving order.",
            "Describe differences between list, tuple and set and give use-cases."
        ]
    elif any(fr in tech_lower for fr in ["django", "flask", "fastapi"]):
        templates = [
            f"What are the differences between synchronous and asynchronous request handling in {tech}?",
            f"How do you structure a {tech} app for scalability and maintainability?",
            f"Explain how authentication and authorization are commonly implemented in {tech}.",
            f"Describe how to test endpoints and database interactions in a {tech} application."
        ]
    elif any(db in tech_lower for db in ["mysql", "postgres", "mongodb", "sqlite"]):
        templates = [
            "Design indexes for a table storing 10 million user records — what columns do you index and why?",
            "Explain ACID properties and how they differ from BASE in NoSQL databases.",
            "How do you backup and restore a large database with minimal downtime?",
            "Write an efficient query to paginate results and explain its performance implications."
        ]
    elif "react" in tech_lower or "vue" in tech_lower or "angular" in tech_lower:
        templates = [
            f"Explain virtual DOM and how {tech} optimizes UI rendering.",
            "How do you manage state in a large frontend application? Compare approaches.",
            "Describe how you would test a complex component.",
            "How do you optimize bundle size and load time in modern frontend apps?"
        ]
    else:
        templates = [
            f"Explain the core concepts of {tech} and typical use-cases.",
            f"Describe a challenging bug you might encounter using {tech} and how to debug it.",
            f"How would you measure proficiency in {tech} during a live coding or take-home test?",
            f"List performance pitfalls with {tech} and ways to mitigate them."
        ]
    for i in range(count):
        questions.append(templates[i % len(templates)])
    return questions


def generate_questions_via_llm(tech_list: List[str], per_tech: int = 4) -> Dict[str, List[str]]:
    """
    Use Gemini to generate 3-5 questions per technology. If not configured, use fallback.
    Returns dict: {tech: [q1, q2, ...], ...}
    """
    results = {}
    techs_str = ", ".join(tech_list)
    system = (
        "You are an expert technical interviewer. For each technology or tool listed, "
        "generate between 3 and 5 clear technical screening questions. "
        "Return JSON where keys are the technology names and values are arrays of questions. "
        "Prefer variety: conceptual, practical (code/architecture), debugging, and advanced."
    )
    user_prompt = (
        f"Technologies: {techs_str}\n\n"
        f"Respond only with valid JSON object mapping technology to list of questions.\n"
        f"Example:\n{{\n  \"Python\": [\"q1\",\"q2\",...],\n  \"Django\": [\"q1\",\"q2\",...]\n}}\n"
    )

    try:
        text = call_gemini_chat(system, user_prompt)
        try:
            parsed = json.loads(text)
            for tech in tech_list:
                key_candidates = [k for k in parsed.keys() if k.lower() == tech.lower()]
                if key_candidates:
                    results[tech] = parsed[key_candidates[0]][:per_tech]
                else:
                    results[tech] = fallback_generate_questions(tech, count=per_tech)
            return results
        except Exception:
            pass
    except Exception:
        pass

    # fallback only
    for tech in tech_list:
        results[tech] = fallback_generate_questions(tech, count=per_tech)
    return results
