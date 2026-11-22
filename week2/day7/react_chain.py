import os
import re
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

# Tool

def get_product_prince(product):
    if product == "Iphone 17":
        return 1500
    elif product == "Iphone 16":
        return 1200
    else:
        return "Product not found"
    

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "Invalid expression"
    
tools = {
    "get_product_prince": get_product_prince,
    "calculator": calculator
}
    
system_prompt = """
you are a shopping assistant.
you have these tools:
get_product_prince(product) - returns the price of the product
calculator(expression) - evaluates a mathematical expression
IMPORTANT: 
Call tool exectly like this example:
Action: get_product_prince("Iphone 17")
Action: calculator("1500 + 200")

Never write:
get_product_prince(product = "Iphone 17")

Never write:
calculator(expression = "1500 + 200")

Follow these rules:

1.Decide what you need to do next
2.Call only one tool at a time
3.After writy an action, STOP immediately 
4.Never guess or invent a tool result.
5.wait unit you recieve an observation
6.Then decide your next action
7.when the tast is complete, give the Final Anser.

Format:
Thought: What you need to do
Action: tool_name("Arguments")

When finished:

Final Answer: Your Answer

"""

def run_agent(question):

    message = [
        {
            "role" : "system",
            "content" : system_prompt
        },
        {
            "role" : "user",
            "content" : question
        }
    ]
    for step in range(5):

        print("\n------------------------------------")
        print(f"Step {step + 1}:") 
        print("------------------------------------")

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=message,
            temperature=0,
            )
        
        answer = response.choices[0].message.content

        print(answer)

        # Agent is Finished
        if "Final Answer:" in answer:
            break

        # Finish the action 
        match = re.search(r"Action: (\w+)\((.*)\)", answer)
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2)
            tool_input = tool_input.strip()
            tool_input = tool_input.strip('"')

            # RUN THE TOOL
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = f"Tool {tool_name} not found"

            print("\nObservation:", observation)

            # Add LLM response to memory
            message.append({"role": "assistant", "content": answer})

            # Give tool REsult back to the llm

            message.append({"role": "user", "content": "Observation: " + str(observation)})
            sleep(5)

prompt = """
I have 5000 rupees. what is the price of the Iphone 17 and  I want to buy it. Can you tell me how much money I will have left after buying the iphone 17?
"""
run_agent(prompt)