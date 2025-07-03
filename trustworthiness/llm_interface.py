from .models import GEMINI_DEFAULT_MODEL, GEMINI_SUPPORTED_MODELS
from typing import List, Dict

import litellm

def call_llm(messages: List[Dict[str, str]],
             model: str = GEMINI_DEFAULT_MODEL,
             api_key: str = None,
             budget: int = None
    ) -> str:
    try:

        config = {"api_key": api_key} if api_key else {}

        if model.startswith("gemini") and budget and "thinking" in GEMINI_SUPPORTED_MODELS[model]:
            thinking = {"type": "enabled", "budget_tokens": budget}
            response = litellm.completion(
                model=model,
                config=config,
                messages=messages,
                thinking=thinking,
            )
        else:
            response = litellm.completion(
                model=model,
                config=config,
                messages=messages
            )
        return response['choices'][0]['message']['content'].strip()
    except Exception as ex:
        raise RuntimeError(f"LLM call failed: {ex}")
