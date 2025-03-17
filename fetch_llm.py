import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("SAMBANOVA_API_KEY")

client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="Meta-Llama-3.1-70B-Instruct",
    messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Hello"}],
    temperature=0.1,
    top_p=0.1
)

print(response.choices[0].message.content)