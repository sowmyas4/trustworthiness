from trustworthiness.evaluator import LLMEvaluator
import os

if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    evaluator = LLMEvaluator(api_key=api_key)
    evaluator.set_model("gemini/gemini-2.0-flash-lite-preview-02-05")
    result = evaluator.evaluate_answer("What is 1 + 1?")
    print("Certainty score:", result["certainty_score"])
    print("LLM response:", result["raw_response"])
