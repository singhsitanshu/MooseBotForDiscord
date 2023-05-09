import openai
import os

openai.api_key = "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"
model_engine = "davinci"
prompt = "What were the events in the American Revolution?"
max_length = 1000

response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_length
)

print(response.choices[0].text)