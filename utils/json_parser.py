import json
import re

def extract_json(text):
    # Handle list response from new Gemini models
    if isinstance(text, list):
        for item in text:
            if isinstance(item, dict) and 'text' in item:
                text = item['text']
                break

    # Handle object with .content attribute (LangChain message)
    if hasattr(text, 'content'):
        text = text.content

    # If still a list after content extraction
    if isinstance(text, list):
        for item in text:
            if isinstance(item, dict) and 'text' in item:
                text = item['text']
                break

    # Convert to string if needed
    if not isinstance(text, str):
        text = str(text)

    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from within text
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Invalid JSON from LLM: {text}")