import os   #load desktop functionalities
from pathlib import Path
from dotenv import load_dotenv  #loading api_key wagera
from groq import Groq
from time import sleep


load_dotenv()  #load .env file
my_api_key = os.getenv("GROQ_API_KEY")  #get api_key from .env file

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

client = Groq(api_key=my_api_key)  #initialize groq client with api_key
model="llama-3.3-70b-versatile"  #set model to use
prompt="Explain how internet works."
message={
    "role":"user",
    "content": prompt
}
messages=[message]
# response1=client.chat.completions.create(model=model,messages=messages)
# print(response1)
# answer=response1.choices[0].message.content
# print(answer)

#above done without streaming
stream=client.chat.completions.create(model=model,messages=messages,stream=True)

for chunk in stream:
    content=chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)