import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  #384 length vector
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it in your .env file.")
client = Groq(api_key=my_api_key)
groq_model = "openai/gpt-oss-120b" 

documents = [
    "Employees receive 24 days of paid leave per year.",
    "The company offers a comprehensive health insurance plan.",
    "Employees can work remotely up to two days a week.",
    "The company provides a retirement savings plan with matching contributions.",
    "Employees are eligible for performance-based bonuses.",
    "The company has a flexible work schedule policy.",
    "Employees can participate in professional development programs.",
    "The company offers wellness programs and gym memberships.",
    "Employees have access to mental health support services.",
    "The company provides parental leave for new parents.",
]

embeddings = model.encode(documents)
def cosine_similarity(a,b): #comparison
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def retrieve(query_embedding):
    scores = []
    for i,document in enumerate(embeddings):
        score=cosine_similarity(query_embedding, document)
        scores.append((score,documents[i]))
    scores.sort(reverse=True)
    return scores[0] #HIGHEST SCORE

def ask_llm(question,context):
    sys_prompt = f"""answer in one line only .Answer only based on the context provided. If the answer is not in the context,do not hallucinate.Context:{context}"""
    system_message={
        "role": "system",
        "content": sys_prompt
    }
    message={
        "role": "user",
        "content": question
    }
    messages=[system_message, message]
    response = client.chat.completions.create(model=groq_model, messages=messages)
    answer = response.choices[0].message.content
    return answer

query="How many paid leave days do employees get?"
query_embedding = model.encode(query)
score, context = retrieve(query_embedding)
answer = ask_llm(query, context)
print(answer)
