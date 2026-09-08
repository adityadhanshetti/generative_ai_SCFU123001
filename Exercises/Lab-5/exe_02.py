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
abstract = input("Enter Abstract : ")


# Initialize LLM
llm = ChatOllama(model=MODEL)


# Prompt 1: Extract complaint details
extract_prompt = PromptTemplate.from_template(
    """
    Extract the following information from the Research paper abstract:

    1. Research Question
    2. Method
    3. Key Findings

    Return the information in a clear structured format.

    Customer Review:
    {abstract}
    """
)


# Prompt 2: Generate support ticket
summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional Science communicator explaining to a general audience."
    ),
    (
        "human",
        """
        Convert the following extracted customer information
        into a professional summary.

        Extracted Complaint:
        {structured_information}
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