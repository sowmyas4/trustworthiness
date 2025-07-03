from . import models
from .llm_interface import call_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMEvaluator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.budget = None
        self.model = models.GEMINI_DEFAULT_MODEL

    def set_model(self, model: str):
        if model not in models.GEMINI_SUPPORTED_MODELS.keys() or len(model) > 45:
            raise ValueError(f"Model {model} is currently not supported. Please selected a different model.")
        self.model = model

    def set_thinking_credits(self, budget: int):
        if budget not in models.GEMINI_THINKING_CREDITS:
            raise ValueError(f"Credit amount {budget} is invalid")
        self.budget = budget

    def sanitize_input(self, text: str) -> str:
        sanitized = text.strip().replace("\n", " ")
        if text != sanitized:
            logger.info(f"Sanitized input: '{text}' -> '{sanitized}'")
        return sanitized

    def validate_input(self, text: str, field_name: str):
        if not text.strip():
            raise ValueError(f"{field_name} cannot be empty or whitespace only.")

    def validate_certainty_answer(self, text: str):
        # LLMs can respond in any format, which may change over time
        if not text.strip():
            raise ValueError(f"LLM returned invalid certainty score ({text}.")

    def build_self_reflection_prompt (self, question: str, answer: str) -> str:
        # Sanitize inputs and assemble the LLM prompt
        question = self.sanitize_input(question)
        answer = self.sanitize_input(answer)

        return (
            f"Statement: {question}\n"
            f"Response: {answer}\n"
            "Do you think of this response to the statement is correct or incorrect, "
            "please pick one of these choices:"
            "(A) Correct (B) Incorrect (C) I am not sure"
        )

    def parse_certainty_score (self, output: str) -> float:
        self.validate_certainty_answer(output)

        # we only care about the last 20 chars of the LLM output,
        # but we want the last split (in case of multiple choice prompt)
        # and then the first char of it will be the score
        output_clean = output.strip()[-20:].lower()
        score = output_clean.split('(')[-1][0]

        if score == 'a':
            return 1.0
        if score == 'c':
            return 0.5

        # if 'b' or we could not parse, return 0 (no confidence)
        return 0.0

    def evaluate_answer (self, prompt: str, answer: str = None) -> dict:
        if answer is None:
            # first ask the LLM the question, then for the trustworthiness score
            sanitized_prompt = self.sanitize_input(prompt)
            messages = [{"role": "user", "content": sanitized_prompt}]
            answer = call_llm(messages, model=self.model, api_key=self.api_key, budget=self.budget)
        else:
            self.validate_input(answer, "Answer")

        self.validate_input(prompt, "Question")

        # Assemble the prompt
        reflection_prompt = self.build_self_reflection_prompt(prompt, answer)
        messages = [{"role": "user", "content": reflection_prompt}]
        output = call_llm(messages, model=self.model, api_key=self.api_key, budget=self.budget)
        certainty_score = self.parse_certainty_score(output)
        return {"certainty_score": certainty_score, "raw_response": answer}