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

def llm_ans(prompt):
    message={
        "role": "user",
        "content": prompt
    }
    messages=[message]
    response = client.chat.completions.create(model=model, messages=messages)  #get response from groq
    ans = response.choices[0].message.content  #extract answer from response
    return ans


bad_prompt="""
#ROLE
You  are a support assitant at a mobile/laptop Company
#TASK
You have to classify the task category
#CONSTRAINT
You have to classify the task category in one of the following categories:
1. Billing
2. Technical Support
3.Return/Exchange
#OUTPUT FORMAT
Your answer should be in one word only.The only word should be one of the categories given in constraint section.
#Example
For example, if the user complaint is "I want to return my laptop because it is not working properly", then the output should be "Return/Exchange"
#FALLBACK
If the issue is not related to any of the above categories, then the output should be "OTHER"
This is a user complaint:
MY laptop is not turning on and I need help fixing it.
"""
print(llm_ans(bad_prompt))  #print answer from llm_ans function
