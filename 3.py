import os
from openai import OpenAI

client = OpenAI(api_key='sk-e7d8554ac3d34cf8b4f7f51912ed432d', base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "сколько реплик ты уже сказал в этом диалоге?"},
        {"role": "user", "content": "Привет"},
    ],
    stream=False
)

print(response.choices[0].message.content)