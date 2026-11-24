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

documnet_embedding = model.encode(documents)

def cosine_similarity(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
        )

query = "haw much vecation do i get "