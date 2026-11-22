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
# 3 prompt
prompt1 = "hi!"
prompt2 = "Suggest me a name for my clothing company"
prompt3 = "what you think about sam altman?"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
    "role": role,
    "content": prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens = 100)
    usage = response.usage
    print(f"Prompt: {prompt}--> your tokens: {usage.prompt_tokens}, Completion tokens: {usage.completion_tokens}, total tokens: {usage.total_tokens}, finish reason: {response.choices[0].finish_reason}")



#messages = [message]
#response = client.chat.completions.create(model=model, messages=messages)
#print(response)

#print("###############################")

#answer = response.choices[0].message.content
#print(f"Fun fact about llamas: {answer}")
