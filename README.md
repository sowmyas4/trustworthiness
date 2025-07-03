# ai-uncertainty-estimator
Package to query an LLM and return answer while estimating the uncertainty of that answer.
It evaluates the self-reflection certainty score of LLM-generated answers based on the Cleanlab ACL'24 paper.

## Install

```bash
git clone git@github.com:sowmyas4/ai-uncertainty-estimator.git .
cd ai-uncertainty-estimator
python3 -m venv .venv
pip3 install litellm
```

## Simple Demo
Please see demo.py

## Config

This implementation uses `litellm` to support multiple providers (e.g., Gemini, OpenAI).
The recommended connection is using a Gemini API key (not provided) and passing
it in when initiating the LLMEvaluator object (see demo.py for more details).

An alternate option is to set the Gemini API key as an environment variable
(shown below) and run the code as outlined in demo.py:
```bash
export GEMINI_API_KEY="your-key"
```

This implementation currently only supports Gemini but may easily be extended
to support other LLMs.

Please see the LiteLLM documentation for supported models:
https://docs.litellm.ai/docs/providers/gemini#chat-models

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