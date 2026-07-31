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

JD="""
We are hiring a software engineer with experience in Python and JavaScript. The ideal candidate should have a strong understanding of web development frameworks, RESTful APIs, and database management. Responsibilities include developing and maintaining web applications, collaborating with cross-functional teams, and ensuring the performance and scalability of our software solutions.
requirements:
- Proficiency in Python and JavaScript
- Experience with web development frameworks such as Django or Flask
- Knowledge of RESTful APIs and database management
- Strong problem-solving skills and attention to detail
- Excellent communication and teamwork abilities
- Bachelor's degree in Computer Science or a related field
"""
RESUME="""
Name: John Doe
Email: john.doe@example.com
experience:
- Software Engineer at XYZ Company (2018 - Present)
- Developed and maintained web applications using Python and JavaScript
- Collaborated with cross-functional teams to design and implement new features
- Optimized application performance and scalability
skils:
- Proficient in Python and JavaScript
- Experience with web development frameworks such as Django and Flask
- Knowledge of RESTful APIs and database management

projects:
- E-commerce platform: Developed a full-stack e-commerce application using Django and React, implementing features
- such as user authentication, product catalog, and shopping cart functionality.
- Social media application: Built a social media platform using Flask and Vue.js, allowing users to create profiles, post updates, and interact with other users.

Deployed and maintained applications on cloud platforms such as AWS and Heroku, ensuring high availability and scalability.
"""

def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }   
    user_msg = {
        "role": "user", 
        "content": user_prompt
    }
    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

def step1_res_extract(RESUME):
    system_prompt="""
    Give out the details from the resume only , provide accurate information and don't add anything by yourself
    """
    user_prompt=f"""
    Extract the information from this resume
    {RESUME}
    """
    return ask_llm(system_prompt,user_prompt)

def step2_JD_extract(JD):
    system_prompt="""
    You are a professional HR ASSISTANT .Extract the skills from the job description provided.
    only return the skills no other information.Do not invent anything from your side.
    """
    user_prompt=f"""
    Extarct the skills from this jd
    {JD}
    """
    return ask_llm(system_prompt,user_prompt)

def step3_compare(candidate,jd):
    system_prompt="""
    you are an hr assistant . compare the skills of the candidate and the skills required in the jd and produce a final score between 1 to 100 . also give a short verdict whether candidate is a good fit for the job or not.
    """

    user_prompt=f"""
    Compare and match the skills 
    JD:
    {jd}
    candidate:
    {candidate}
    """
    return ask_llm(system_prompt,user_prompt)

candidate=step1_res_extract(RESUME)
sleep(2)
jd=step1_res_extract(JD)
sleep(2)
score=step3_compare(candidate,jd)
print(score)