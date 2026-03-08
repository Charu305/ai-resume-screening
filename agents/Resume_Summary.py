from utils.gemini import get_llm_flash
from utils.json_parser import extract_json

def resume_summarizer(state: dict) -> dict:
    llm = get_llm_flash()

    resume_text = state.get("resume_text")
    if resume_text is None:
        raise ValueError("resume_text missing in state")

    # Optional hard truncation (extra savings)
    resume_text = resume_text[:2000]

    prompt = f"""
    Extract ONLY:
    - skills (list)
    - years_of_experience (number)
    - key_projects (max 3)

    Resume:
    {resume_text}

    Return STRICT JSON only.
    """

    raw = llm.invoke(prompt).content
    summary = extract_json(raw)

    return {
        **state,
        "resume_summary": summary
    }
