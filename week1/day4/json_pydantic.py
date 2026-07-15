import os   #load desktop functionalities
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv  #loading api_key wagera
from groq import Groq

load_dotenv()  #load .env file
my_api_key = os.getenv("GROQ_API_KEY")  #get api_key from .env file

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

client = Groq(api_key=my_api_key)  #initialize groq client with api_key
model="llama-3.3-70b-versatile"  #set model to use
role="user"  #set role to user
#structure it
from pydantic import BaseModel  #import BaseModel from pydantic
from typing import Optional  #import Optional from typing
class Ticket(BaseModel):
    name: str
    email: Optional[str]= None
    phone: Optional[str]= None
    issue: str

schema=Ticket.model_json_schema()  #get json schema from Ticket model

response_format={
    "type":"json_object"
}
system_prompt=f"""
Extract the personal information from the customer ticket and return it in the following json format:
{schema}
"""
message_system={
    "role":"system",
    "content":system_prompt
}
text="hello My name is Python, I have an Iphone which stopped working, I need help to fix it,I live on mars "  #set text to send to model
prompt=f""" This is a customer ticket ,please extract the personal information from this.
{text}
"""  #create prompt with text
message = {"role": role, "content": prompt}  #create message with role and prompt
messages=[message_system,message]
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)  #send message to groq client and get response

answer = response.choices[0].message.content  #get answer from response
print(answer)  #print answer

#isko padhte kaise hain
import json
raw_json=answer
date_file=json.loads(raw_json)  #load json from raw_json
ticket=Ticket(**date_file)  #create Ticket object from date_file

print(ticket.name)  #print name from ticket
print(ticket.email)  #print email from ticket
print(ticket.phone)  #print phone from ticket
print(ticket.issue)  #print issue from ticket