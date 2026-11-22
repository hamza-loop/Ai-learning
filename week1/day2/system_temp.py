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
role = "user"
prompt = "Suggest me a name for my clothing company"

#SYSTEM

message_system = {
    "role": "system",
    #"content": "You are my girlfriend .",
    #"content": "You are my stricy office colleague who is also my manager.",
    "content": "you are a brand manager suggest who suggest name for my company. name should be in one word. Suggest one name only"
}
#MESSAGE ME ROLE AND CONTENT
message = {
    "role": role,
    "content": prompt
}

messages = [message_system,message]
# temp bydefault meaning safe and genrally range b/w 0-2. 0 means safe and 2 means creative and risky
response = client.chat.completions.create(model=model, messages=messages, temperature=0)
# print(response)

print("###############################")

answer = response.choices[0].message.content
print(f"{answer}")
