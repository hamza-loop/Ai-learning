import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
        )

model = SentenceTransformer("all-MiniLM-L6-v2") #384
text = "Machine learning is fun "

#embadding  = model.encode(text)
#print(embadding.shape)
#print(embadding[:10])

t1 = "There are 24 paid leave "
# t2 = "There are 24 vacattion days"   # it will give output of 0.4
# t2 = "i love pizza "  # it will give output of 0.05
t2 = "Cat is a wild animal" # it will give outut of 0.022

v1 = model.encode(t1)
v2 = model.encode(t2)

print(cosine_similarity(v1, v2))

