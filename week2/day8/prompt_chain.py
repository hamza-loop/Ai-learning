import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

JD = """
We are hiring a pytho backend developer

REQUIREMENTS:
- strong pyton skills
- Fast API and django 
- PostgreSQL and MySQL 
- Docker 
- Rest API
- AWS
- Two years of experience 
"""

RESUME = """
Name: Rahul Sharma

Experience:
3 year as a python backend developer

Skills:
- Python
- FastAPI
- Django
- mysql
- git

projects:
- Build a food delevery backend using FastAPI and MySQL

Deployed application using Docker

"""

def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }
    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

def step1_res_extract():
    print("STEP 1: Extracting skills from resume...")
    #extract skills from resume
    system_prompt = """
    you are professinol HR assistant. Extract the skills from the resume provided. 
    only return skill no other information. Do not invent skill by yourself.
    """

    user_prompt = f"""
    Extract skills from the following resume:{RESUME}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract():
    print("STEP 2: Extracting skills from job description...")
    #extract skills from JD
    system_prompt = """
    you are professinol HR assistant. Extract the skills from the resume provided. 
    only return skill no other information. Do not invent skill by yourself.
    """

    user_prompt = f"""
    Extract skills from the following job description:{JD}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate,jd):
    print("STEP 3: Matching candidate skills with job description skills...")
    system_prompt = """
    you are professinol HR assistant. You have to match the candidate skills with the job description skills and profuce a final score. The score should be in percentage and also produce a short verdict on the candidate suitability for the job.
    """

    user_prompt = f"""
    compare the match the skills of the candidate with the skills required in the job description. Candidate skills: {candidate}. Job description skills: {jd}
    """
    return ask_llm(system_prompt, user_prompt)

candidate_skills = step1_res_extract()
print(candidate_skills)
sleep(2)

jd = step2_JD_extract()
print(jd)
sleep(2)

score = step3_match(candidate_skills, jd)

print(score)
