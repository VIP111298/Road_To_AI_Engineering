import json
import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)

model = "llama-3.3-70b-versatile"


class ResumeData(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]


schema = ResumeData.model_json_schema()

system_prompt = f"""
You are a resume information extractor.

Return only a JSON object matching this schema:

{schema}

Rules:
- Do not invent information.
- Return null when email or phone is missing.
- Return an empty list when any list field is missing.
"""

resume_text = """
Vipul Tiwari
Email: vipul@example.com

Skills:
Python, C++, HTML, CSS, Git

Education:
B.Tech CSE AI & ML, KIET Group of Institutions

Projects:
Crop Disease Detection
Face Recognition Attendance System

Experience:
MLSA Team Lead
"""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": f"Extract information from this resume:\n\n{resume_text}"
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format={"type": "json_object"}
)

answer = response.choices[0].message.content

data = json.loads(answer)

resume = ResumeData(**data)

print("Name:", resume.name)
print("Email:", resume.email)
print("Phone:", resume.phone)
print("Skills:", resume.skills)
print("Education:", resume.education)
print("Experience:", resume.experience)
print("Projects:", resume.projects)