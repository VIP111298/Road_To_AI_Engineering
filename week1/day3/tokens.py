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
prompt1="Hi!"
prompt2="Expalin Time Travel in detail"
prompt3="Write a 1000 word essay on the impact of climate change on global agriculture."
prompts=[prompt1,prompt2,prompt3]
for prompt in prompts:
    message_system={
    "role": "user",
    "content": prompt
    }
    message = [message_system]  #create message with role and prompt
    response = client.chat.completions.create(model=model, messages=message,max_tokens=50 )  #send message to groq client and get response
    usage=response.usage
    print(f"Prompt: {prompt} --> usage.prompt_tokens: {usage.prompt_tokens}, usage.completion_tokens: {usage.completion_tokens} total_tokens: {usage.total_tokens} finished: {response.choices[0].finish_reason} ")
#messages={"role": role, "content": prompt}  #create message with role and prompt
#prompt="Suggest a name for my clothing company"
#message_system={
 #   "role": role,
  #  "content": prompt
#}
#message = [messages]  #create message with role and prompt
#temperature by default is 0 , meaning safe.
#response = client.chat.completions.create(model=model, messages=message, temperature=1)  #send message to groq client and get response
