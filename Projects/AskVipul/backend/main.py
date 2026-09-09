import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader
BASE_DIR = Path(__file__).resolve().parent

RESUME_PATH = (
    BASE_DIR.parent
    / "Vipul_Tiwari_Resume.pdf"
)
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

model = "openai/gpt-oss-20b"
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []
resume_schema = Resume.model_json_schema()
cached_resume: Resume | None = None

class ChatRequest(BaseModel):
    question: str

def ask_candidate(question: str, resume: Resume):

    system_prompt = f"""
You are AskVipul, the AI portfolio assistant for Vipul Tiwari.

Verified resume data:

{resume.model_dump_json(indent=2)}

STRICT RESPONSE RULES:

1. Use only the verified resume data.
2. Never invent information.
3. Return plain text only.
4. Do not use Markdown, HTML, tables or headings.
5. Never use **, #, |, <br>, backticks or numbered lists.
6. Maximum response length is 100 words.
7. Start with one direct sentence.
8. After that, include at most four short bullet points.
9. Start each bullet with this character: •
10. Put every bullet on a separate line.
11. Do not repeat information.
12. Refer to Vipul in the third person.
13. If information is unavailable, say:
"I don't have verified information about that."
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],

        temperature=0.1,
        reasoning_effort="low",
        max_completion_tokens=400
    )

    answer = response.choices[0].message.content

    return answer.strip()
def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format,
    reasoning_effort="low",
    temperature=0,
    max_completion_tokens=1500
    ) 
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume

def read_pdf(file_path: Path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def get_resume():

    global cached_resume

    if cached_resume is None:

        print("Resume pehli baar parse ho raha hai...")

        resume_text = read_pdf(RESUME_PATH)

        cached_resume = parse_resume(resume_text)

        print("Resume parse hokar memory mein save ho gaya.")

    return cached_resume

@app.get("/")
def home():
    # resume_text=read_pdf(Path("my_resume.pdf"))
    # resume=parse_resume(resume_text)
    return {
        "message" : "Ye home page hai"
    }



@app.post("/chat")
def chat(request: ChatRequest):

    resume = get_resume()

    answer = ask_candidate(
        request.question,
        resume
    )

    return {
        "answer": answer
    }
