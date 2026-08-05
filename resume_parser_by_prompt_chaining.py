import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
from time import sleep

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api error")

model = "llama-3.3-70b-versatile"
client = Groq(api_key = my_api_key)

JD = """
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
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
    response = client.chat.completions.create(model = model, messages= messages)
    answer = response.choices[0].message.content
    return answer

def step1_res_extract():
    # extract skills from resume
    
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the candidate's provided resume.
    Only return the skills, no other information. Do not invent any information by yourself.
    OUTPUT FORMAT:
    skills should be seperated by commas. just return comma seperated skills do not return any other filler information.
    """

    user_prompt = f"""
    Extract the skills from this resume {RESUME}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract():
    # extract skills from JD
    
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the provided job description.
    Only return the skills, no other information. Do not invent any information by yourself.
    OUTPUT FORMAT:
    skills should be seperated by commas. just return comma seperated skills do not return any other filler information.
    """

    user_prompt = f"""
    Extract the skills from this JD {JD}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate,jd):
    system_prompt = """
    You are a professional HR assistant. Compare all the skills of candidate and the skills required in the job description and produce a final score b/w 1 to 100. Also produce a short verdict whether the candidate is a good fit for the role or not.
    """
    user_prompt = f"""
    Compare and match the skills
    JD: {jd}
    Candidate: {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate = step1_res_extract()
sleep(2)
jd = step2_JD_extract()
print(jd) #debugged here!!!
sleep(2)
score = step3_match(candidate,jd)
print(score)
