import os   #load desktop functionalities
from pathlib import Path
from dotenv import load_dotenv  #loading api_key wagera
from groq import Groq

load_dotenv()  #load .env file
my_api_key = os.getenv("GROQ_API_KEY")  #get api_key from .env file

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

client = Groq(api_key=my_api_key)  #initialize groq client with api_key
model="llama-3.3-70b-versatile"  #set model to use
role="user"  #set role to user
prompt="Do you Know G wagon?"
message = [{"role": role, "content": prompt}]  #create message with role and prompt
response = client.chat.completions.create(model=model, messages=message)  #send message to groq client and get response
print(response)

print("##########################")
answer = response.choices[0].message.content  #get answer from response
print(answer)  #print answer