import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it in your .env file.")
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

#step1
knowledge_base={
    "age":"The age of Vipul is 21 years.",
    "name":"The name of the person is Vipul."
}

#step2:retreival
def retrieve_info(question):
    question=question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "name" in question:
        return knowledge_base["name"]
    else:
        return "I don't have information about that."

def ask_llm(question):
    context = retrieve_info(question)
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
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

question = "Do you know the age of Vipul?"
print(ask_llm(question))