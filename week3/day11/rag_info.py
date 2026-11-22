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

# here we make knowlledgebase for the model to answer questions from
# STEP1
knowledge_base = {
    "age" : "the age of hamza is 23 year",
    "networth" : "the networth of hamza is 1 million dollars"

}
#STEP 2 
def retrieve_info(question):
    question = question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "networth" in question:
        return knowledge_base["networth"]
    else:
        return "I don't have information on that topic."
    

def ask_llm(question):
    context = retrieve_info(question)

    system_prompt = f"""answer in one line, answer the question based on the context provided, if the context is not enough to answer the question then say 'I don't have information on that topic. context: {context}"""
    system_message = {
        "role": "system",
        "content": system_prompt
    }
    message = {
        "role" : "user",
        "content" : question
    }
    messages = [system_message, message]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

question = "what is the hamza age?"
print(ask_llm(question))
