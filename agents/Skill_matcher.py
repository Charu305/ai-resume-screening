from utils.gemini import get_llm_flash
from utils.json_parser import extract_json

def skill_match(state: dict) -> dict:
    llm = get_llm_flash()

    jd = state.get("jd_analysis")
    resume_summary = state.get("resume_summary")

    if jd is None or resume_summary is None:
        raise ValueError("jd_analysis or resume_summary missing in state")

    prompt = f"""
    You are evaluating a candidate for a job.

    Job requirements:
    {jd}

    Candidate profile:
    {resume_summary}

    Return STRICT JSON only:
    {{
      "match_score": number between 0 and 1,
      "strengths": list (max 3),
      "gaps": list (max 2)
    }}
    """

    raw = llm.invoke(prompt).content
    skill_analysis = extract_json(raw)

    return {
        **state,
        "skill_analysis": skill_analysis
    }
