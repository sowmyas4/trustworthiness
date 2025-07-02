# ai-uncertainty-estimator
Package to query an LLM and return answer while estimating the uncertainty of that answer.
It evaluates the self-reflection certainty score of LLM-generated answers based on the Cleanlab ACL'24 paper.

## Install

```bash
pip install litellm
pip install trustworthiness
```

## Simple Demo

```python
from trustworthiness.evaluator import LLMEvaluator

evaluator = LLMEvaluator("Gemini API key")
result = evaluator.evaluate_answer("What is 1 + 1?", "2")
print(result)
```

## Config

This implementation uses `litellm` to support multiple providers (e.g., Gemini, OpenAI).
You can set your model key as an environment variable:

```bash
export GEMINI_API_KEY="your-key"
```

This implementation currently only supports Gemini but may easily be extended
to support other LLMs.

## Testing

Run unit tests using:

```bash
pytest tests/
```

## Contributing and Maintaining

Long-term discussion and bug reports are maintained via GitHub Issues.
Code review is done via GitHub Pull Requests.

This file will be updated with more details if the project should continue.

Full writeup of development process can be found in writeup.md