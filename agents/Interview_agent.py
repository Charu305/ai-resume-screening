from utils.gemini import get_llm_flash

def generate_interview_questions(state: dict) -> dict:
    llm = get_llm_flash()

    skill_analysis = state.get("skill_analysis")
    if skill_analysis is None:
        raise ValueError("skill_analysis missing in state")

    prompt = f"""
    Based on the following candidate analysis:
    {skill_analysis}

    Generate:
    - 2 technical interview questions
    - 1 scenario-based interview questions

    Keep each question under 25 words.
    No explanations.
    Return them as clear, readable text.
    """

    questions = llm.invoke(prompt).content

    # ✅ MUST return dict
    return {
        **state,
        "interview_questions": questions
    }
