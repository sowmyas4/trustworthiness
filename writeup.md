# Overview
I started by created a GitHub directly to put my code. I then created the
framework for the package (renaming the package 2x in the process, of course).

Once the basics were done, I looked into how to connect to `litellm`.

In-between I consulted with ChatGPT and compared its code to my own.
For example, I liked ChatGPT's package name of "trustworthiness", rather
than my "uncertainty_estimator", the former being more catchy and less
"on the nose".

# Objectives
My main design objectives were simplicity of code, modularity, and
potential extendability.

# Sanitization of user input
I thought a lot about sanitization of user input. The "regular" usecases
of SQL injection, malicious code, or HTML escape characters did not apply
since I was running it in the LLM. I went through the LiteLLM documentation
and noticed that they already sanitize on their end, specifically to prevent
malicious input. At the end, I decided to rely on the LiteLLM sanitization,
removing only newlines on my end.

# Tradeoffs
- LLM key: since this is a library package, the user should be able to pick
which LLM they wanted to use. And if they are picking an LLM, they should
be able to pass in their own API key, to integrate with their own password
management system.
- Retry: Given that the call is using their own LLM API key, and given how
expensive LLM credits can be (at the time of writing), I opted to make the
retry mechanism optional.
- Validation of LLM output: I was initially going to add more validation
to the LLM output, but I noticed that LLM may respond with different formats
(and it may change over time). So I opted just to remove the newlines
from the output and return 0.0 confidence if the output could not be parsed.

This took me a little less than 2 hours to do the functional work, but I took
an additional couple hours to experiment with different elements and have
some fun with it.