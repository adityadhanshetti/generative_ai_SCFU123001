from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor

MODEL = "llama3.1:8b"
llm = ChatOllama(model=MODEL)


def cgpa_to_marks(cgpa:float) -> float:
    """Convert CGPA into marks."""
    return round(cgpa * 9.5, 4)

class CgpaInput(BaseModel):
    cgpa: float = Field(description="The CGPA to convert into marks")

cgpa_to_marks_tool = StructuredTool.from_function(
    func=cgpa_to_marks,
    name="CGPA_TO_MARKS",
    description="Convert CGPA into marks",
    args_schema=CgpaInput
)

def marks_to_cgpa(marks:float) -> float:
    """Convert marks into CGPA."""
    return round(marks / 9.5, 4)

class MarksInput(BaseModel):
    marks: float = Field(description="The marks to convert into CGPA")

marks_to_cgpa_tool = StructuredTool.from_function(
    func=marks_to_cgpa,
    name="MARKS_TO_CGPA",
    description="This function converts marks into CGPA",
    args_schema=MarksInput
)

tools = [cgpa_to_marks_tool, marks_to_cgpa_tool]
tool_lookup = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

user_request = (
    "HI"
)
messages = [HumanMessage(content=user_request)]

# The model decides which tools to call and supplies validated arguments.
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

if not ai_response.tool_calls:
    print(ai_response.content)
else:
    # Run every requested tool at the same time.
    with ThreadPoolExecutor(max_workers=len(ai_response.tool_calls)) as executor:
        futures = [
            executor.submit(
                tool_lookup[tool_call["name"]].invoke,
                tool_call["args"],
            )
            for tool_call in ai_response.tool_calls
        ]

        for tool_call, future in zip(ai_response.tool_calls, futures):
            messages.append(
                ToolMessage(
                    content=str(future.result()),
                    tool_call_id=tool_call["id"],
                )
            )

    # Give the tool results back to the model for a final answer.
    final_response = llm_with_tools.invoke(messages)
    print(final_response.content)





