import json
import re

def extract_json(text: str) -> dict:
    """
    Extract JSON from LLM responses that may contain markdown.
    """
    try:
        # Remove ```json ``` wrappers
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except Exception as e:
        raise ValueError(f"Invalid JSON from LLM: {text}") from e