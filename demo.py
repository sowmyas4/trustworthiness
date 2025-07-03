from trustworthiness.evaluator import LLMEvaluator

if __name__ == "__main__":
    import os
    api_key = os.getenv("GEMINI_API_KEY")
    evaluator = LLMEvaluator(api_key=api_key)
    result = evaluator.evaluate_answer("What is 1 + 1?", "2")
    print("Certainty score:", result["certainty_score"])
    print("LLM response:", result["raw_response"])
