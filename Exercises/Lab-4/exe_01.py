## Exercise 1 — Job Posting to Candidate Outreach Pipeline

# Build a 2-step pipeline. Step 1 extracts the key requirements from a raw job posting into structured form. Step 2 generates a personalized outreach message for a specific candidate, using the structured requirements from Step 1, not the raw posting.

# **Input:** `job_posting_text`, `candidate_profile`

# **Output:** the structured requirements from Step 1, and the personalized outreach message from Step 2


import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

REQ_EXTRACTOR_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
OUTREACH_MODEL = "deepseek-ai/deepseek-v4-flash-0731"

REQ_EXTRACTOR_SYSTEM_PROMPT = """
You extract key requirements from job postings. Return valid JSON only with these fields:

{
  "job_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "years_of_experience": "",
  "education": "",
  "responsibilities": [],
  "location": "",
  "employment_type": ""
}

Use only information stated in the job posting. Do not invent or infer missing details. Use empty strings or empty arrays when information is unavailable.
"""


OUTREACH_SYSTEM_PROMPT = """
You write concise, professional, and personalized recruitment outreach messages. Use only the structured job requirements and candidate profile provided in the user message. Do not refer to or request the original job posting. Mention relevant connections between the candidate’s experience and the role, but do not exaggerate or invent qualifications. Return only the outreach message.
"""


client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY")
)

job_posting_text = input("Enter JD : ")
candidate_profile = input("Enter Candidate Profile : ")




def chat_completion(message, model):
  completion = client.chat.completions.create(
    model=model,
    messages=message,
    temperature=1,
    top_p=0.95,
    max_tokens=1023,
    # extra_body={"chat_template_kwargs":{"thinking":False,"reasoning_effort":"low"}},
    stream=False
  )

  return completion.choices[0].message.content

requirements_messages = [
  {
    "role": "system",
    "content": REQ_EXTRACTOR_SYSTEM_PROMPT,
  },
  {
    "role": "user",
    "content": f"Job posting:\n{job_posting_text}",
  },
]
requirements_text = chat_completion(requirements_messages, REQ_EXTRACTOR_MODEL)

# requirements = json.loads(requirements_text)

outreach_messages = [
  {
    "role": "system",
    "content": OUTREACH_SYSTEM_PROMPT,
  },
  {
    "role": "user",
    "content": (
      "Structured job requirements:\n"
      f"{requirements_text}\n\n"
      "Candidate profile:\n"
      f"{candidate_profile}"
    ),
  },
]
outreach_message = chat_completion(outreach_messages, OUTREACH_MODEL)
print("Structured requirements:")
print(requirements_text)
print("\nPersonalized outreach message:")
print(outreach_message)