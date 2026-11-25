import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2") #384

groqmodel = "openai/gpt-oss-120b"

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)

documents = [
    "Employee recieve 24 days of paid leave per year",
    "Employee worf from the office on tuesday wednesday and thursday",
    "Employee can work from home on monday and friday",
    "Employee recieve Rs 3000 per month for gym membership",
    "Employee can claim Rs 2000 per month for home internet",
    "Employee have the 90 days of notice period"
]

document_embedding = model.encode(documents)

def cosine_similarity(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
        )

def retrieve(query_embedding):
    scores = []
    for i, doc_emb in enumerate(document_embedding):
        sim_score = cosine_similarity(query_embedding, doc_emb)
        scores.append((sim_score,documents[i]))
    scores.sort(reverse=True)
    return scores[0]

def ask_llm(question, context):

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
    response = client.chat.completions.create(model=groqmodel, messages=messages)
    answer = response.choices[0].message.content
    return answer


query = "haw much vecation do i get "

q_embedding = model.encode(query)

score,context = retrieve(q_embedding)
answer = ask_llm(query,context)
print(answer)