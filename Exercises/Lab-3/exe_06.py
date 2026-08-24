## Exercise 6 — Iterative Content Refiner

# Build a prompt that takes a draft and revises it to fix one specific issue, across multiple rounds.

# **Input:** `draft_text`, `issue_to_fix`
# **Output:** a revised version of the text that resolves that specific issue, run for at least 3 rounds



from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """
You are an expert content editor.

Revise the provided draft to fix only the specific issue identified by the user.

Rules:
- Preserve the draft's original meaning, facts, structure, and overall voice unless changing them is necessary to fix the stated issue.
- Make a focused, meaningful improvement rather than rewriting unrelated sections.
- Do not introduce unsupported facts, opinions, or new ideas.
- Check that the requested issue has been fully resolved before responding.
- Treat each request as one refinement round; improve the current draft again when it is submitted in a later round.
- Return only the revised draft, without explanations, labels, analysis, or editing notes.
"""

draft_text = input("Enter Draft Text : ")
issue_to_fix = input("Enter Issue need to fix : ")

MODEL = "openai/gpt-oss-20b"
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
    {
        "role":"system",
        "content":SYSTEM_PROMPT
    },
    {
        "role":"user",
        "content":"Draft Text : "+draft_text+"\n"+"Issue to be fixed :"+issue_to_fix
    }
]
chat_completion = client.chat.completions.create(messages=messages, model=MODEL)
response = chat_completion.choices[0].message.content
print(response)