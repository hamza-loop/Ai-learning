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

def llm_ans(prompt):
    message = {
        "role": "user",
        "content": prompt
    }

    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer
bad_prompt = """
#ROLE:
You are a support assistant at a company that sells mobile phone and laptops 
#TASKS:
you have to classfy the user complaint into a categories
#CONSTRANTS:
You have to classify the issue in one of these three catogories namely billing, technical, and return
#OUTPUT FORMAT:
our answer should be in one word which belons to the given constraints
#EXAMPLE
for instance if the user complaint is "My phone is not working" then your answer should be technical
#FALLBACK:
if issue does not belong to any of the above categories then your answer should be "other"
My laptop is not working
"""

print(llm_ans(bad_prompt))
