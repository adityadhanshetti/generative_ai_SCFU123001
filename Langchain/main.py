from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.messages import ToolMessage,HumanMessage,AIMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field

MODEL = "llama3.1:8b"
llm = ChatOllama(model=MODEL)


@tool
def multiply( num1:int ,num2:int ) -> int :
    """This tools gives multiplication of num1 and num2"""
    return num1 * num2

# # print(multiply)

# print(multiply.invoke({"num1":5,"num2":10}))

llm_with_tools = llm.bind_tools([multiply])

# print(llm_with_tools.invoke("HI"))

# message = []
# def multiply_agent(userQuery):
#     message.append(HumanMessage(userQuery))
#     aiResponse = llm_with_tools.invoke(message)
#     message.append(aiResponse)
#     if aiResponse.tool_calls :
#         toolResponse = multiply.invoke(aiResponse.tool_calls[0])


@tool
def cgpa(marks:float) -> float :
    """This fucntion converts marks to CGPA """
    return marks/9.5


print(cgpa)

class InputMarks(BaseModel):
    marks : float = Field(description="this fucntion converts marks to cgpa")

StructuredTool.from_function(
    func=cgpa,
    name="CGPA"
    description="This fucntion converts marks into CGPA",
    args_schema=InputMarks
)


