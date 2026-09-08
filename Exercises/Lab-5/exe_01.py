# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
# from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser

# MODEL = "llama3"
# review_text = input("Enter Review Text : ")

# llm = ChatOllama(model=MODEL)

# extract_prompt=PromptTemplate.from_template("Extract the core complaint,product/feature mentioned , and customer sentiment form a raw customer review as structured data. {review_text}")

# generate_ticket_prompt = ChatPromptTemplate.from_messages([
#     ("system","You are a professional support ticket writer"),
#     ("human","{structured_complaint}")
# ])

# chain1 = extract_prompt | llm | StrOutputParser()

# response1 = chain1.invoke({review_text:review_text})

# chain2 = generate_ticket_prompt | llm | StrOutputParser()
# response2 = chain2.invoke({"structured_complaint":response1})



from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


MODEL = "llama3.1:8b"


# Get review from user
review_text = input("Enter Review Text: ")


# Initialize LLM
llm = ChatOllama(model=MODEL)


# Prompt 1: Extract complaint details
extract_prompt = PromptTemplate.from_template(
    """
    Extract the following information from the customer review:

    1. Core complaint
    2. Product or feature mentioned
    3. Customer sentiment

    Return the information in a clear structured format.

    Customer Review:
    {review_text}
    """
)


# Prompt 2: Generate support ticket
generate_ticket_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional customer support ticket writer."
    ),
    (
        "human",
        """
        Convert the following extracted customer complaint
        into a professional support ticket.

        Extracted Complaint:
        {structured_complaint}
        """
    )
])


# Chain 1: Review → Structured Complaint
chain1 = extract_prompt | llm | StrOutputParser()

response1 = chain1.invoke({
    "review_text": review_text
})


# Chain 2: Structured Complaint → Support Ticket
chain2 = generate_ticket_prompt | llm | StrOutputParser()

response2 = chain2.invoke({
    "structured_complaint": response1
})


# Display results
print("\n" + "=" * 50)
print("EXTRACTED COMPLAINT")
print("=" * 50)
print(response1)

print("\n" + "=" * 50)
print("GENERATED SUPPORT TICKET")
print("=" * 50)
print(response2)