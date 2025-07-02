# trustworthiness/llm_interface.py

import litellm
from typing import List, Dict

import os

def call_llm(messages: List[Dict[str, str]], model: str = "gemini/gemini-pro", api_key: str = None) -> str:
    try:
        if api_key is None and model.startswith("gemini"):
            api_key = os.getenv("GEMINI_API_KEY")

        config = {"api_key": api_key} if api_key else {}

        response = litellm.completion(
            model=model,
            config=config,
            messages=messages
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as ex:
        raise RuntimeError(f"LLM call failed: {ex}")
