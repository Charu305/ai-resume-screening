from utils.gemini import get_llm_flash

def final_decision(state: dict) -> dict:
    llm = get_llm_flash()

    analysis = state.get("skill_analysis")

    prompt = f"""
    Based on the following analysis:
    {analysis}

    Decide:
    - SHORTLIST or REJECT
    - confidence (0–1)
    - explanation
    """

    decision = llm.invoke(prompt).content

    return {
        **state,
        "final_decision": decision
    }

