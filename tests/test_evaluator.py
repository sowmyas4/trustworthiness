import pytest
from trustworthiness.evaluator import LLMEvaluator

# Mocking
import trustworthiness.evaluator as evaluator_module
from unittest.mock import patch

def test_sanitize_input():
    evaluator = LLMEvaluator()
    assert evaluator.sanitize_input("  hello\nworld  ") == "hello world"

def test_validate_input_pass():
    evaluator = LLMEvaluator()
    evaluator.validate_input("valid input", "Test Field")  # Should not raise

def test_validate_input_fail():
    evaluator = LLMEvaluator()
    with pytest.raises(ValueError):
        evaluator.validate_input("   ", "Test Field")

def test_build_prompt_sanitizes_and_validates():
    evaluator = LLMEvaluator()
    prompt = evaluator.build_self_reflection_prompt("  What is 2+2?\n", "  4  ")
    assert "What is 2+2?" in prompt
    assert "4" in prompt

def test_parse_certainty_score():
    evaluator = LLMEvaluator()
    assert evaluator.parse_certainty_score("(A)") == 1.0
    assert evaluator.parse_certainty_score("(B)") == 0.0
    assert evaluator.parse_certainty_score("(C)") == 0.5
    assert evaluator.parse_certainty_score("I play by my own rules!") == 0.0

# LLM Functionality tests

def test_evaluate_answer_with_mock():
    evaluator = LLMEvaluator(api_key="dummy-api-key")
    mock_output = "I answer with (A) Correct"
    with patch.object(evaluator_module, "call_llm", return_value=mock_output):
        result = evaluator.evaluate_answer("What is 3 + 2?", "5")
        assert result["certainty_score"] == 1.0
        assert result["raw_response"] == mock_output

    evaluator = LLMEvaluator(api_key="dummy-api-key")
    mock_output = "That would be (C)"
    with patch.object(evaluator_module, "call_llm", return_value=mock_output):
        result = evaluator.evaluate_answer("What is the capital of France?", "Paris")
        assert result["certainty_score"] == 0.5
        assert result["raw_response"] == mock_output

    evaluator = LLMEvaluator(api_key="dummy-api-key")
    mock_output = "That would be (B) Incorrect."
    with patch.object(evaluator_module, "call_llm", return_value=mock_output):
        result = evaluator.evaluate_answer("What is the capital of France?", "Paris")
        assert result["certainty_score"] == 0.0
        assert result["raw_response"] == mock_output