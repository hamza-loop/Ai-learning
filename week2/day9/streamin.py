import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

prompt = "Explain haw internet works"

message = {
    "role" : "user",
    "content" : prompt
}

messages = [message]

# WITHOUT STRAMING
#response1 = client.chat.completions.create(model=model, messages=messages)
#print(response1)
#answer = response1.choices[0].message.content
#print("Answer:", answer)

stram = client.chat.completions.create(model=model, messages=messages,stream=True)

for chunk in stram:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
        
