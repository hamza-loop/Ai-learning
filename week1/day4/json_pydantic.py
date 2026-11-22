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


# Structured prompt to extract personal information from the text
from pydantic import BaseModel, Field
class Ticket(BaseModel):
    name: str = Field(..., description="The name of the customer")
    address: str = Field(..., description="The address of the customer")
    phone_number: str = Field(..., description="The phone number of the customer")
    issue: str = Field(..., description="The issue reported by the customer")

schema = Ticket.model_json_schema()
response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal imformation from the ticket strictly based on this schema, and give the output in JSON format. Do not add any extra information or explanation.
{schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}
text = "Hi my name is John. i have an i phone which is not working properly. I have tried to reset it but it still does not work. Please help me with this issue. my address is from New York and my phone number is 123-456-7890."
prompt = f"""
This is a customer ticket please extract the personal information from text
{text} 
"""

message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

answer = response.choices[0].message.content
print(answer)

# haw any one can read this

import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.address)
print(ticket.phone_number)
print(ticket.issue)  # This will raise an error because 'issue' is not defined in the Ticket model
