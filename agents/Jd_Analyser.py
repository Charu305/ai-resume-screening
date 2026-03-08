from utils.gemini import get_llm
from utils.json_parser import extract_json

def jd_analyzer(state: dict) -> dict:
    llm = get_llm()
    jd_text = state["jd_text"]

    prompt = f"""
    You are a hiring expert.

    Extract the following from the job description:
    - required_skills (list)
    - optional_skills (list)
    - experience_years (number)
    - importance_weights (dict skill -> weight 0-1)

    Job Description:
    {jd_text}

    IMPORTANT:
    - Return ONLY valid JSON
    - Do NOT add explanations
    """

    raw_response = llm.invoke(prompt).content
    jd_analysis = extract_json(raw_response)

    # ✅ Return a dict (LangGraph requirement)
    return {
        **state,
        "jd_analysis": jd_analysis
    }
