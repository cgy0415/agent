# from langchain.tools import tool
# from langchain_openai import ChatOpenAI


# @tool
# def add(a: int, b: int) -> int:
#     """Adds a and b.

#     Args:
#         a: first int
#         b: second int"""

#     return a + b

# @tool
# def multiply(a: int, b: int) ->int:
#     """Multiplies a and b.
    
#     Args:
#         a: first int
#         b: second int"""

#     return a * b 
# tools = [add, multiply]

# llm = ChatOpenAI(model="gpt-4o")
# llm_with_tools = llm.bind_tools(tools)

# query = "3 곱하기 5는 뭔가요? 그리고 2 더하기 4는 뭔가요?"

# response = llm_with_tools.invoke(query)
# # print(response)

# response.tool_calls


# %%
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from operator import add

load_dotenv()

tool = TavilySearch(max_results=2)
tools = [tool]

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    messages: Annotated[list[str], add]
    question: str
    answer: str

graph_builder = StateGraph(
	OverallState,
	input_schema=InputState,
	output_schema=OutputState
)

def chatbot(state: InputState) -> OverallState:
    question = state["question"]
    response = llm.invoke(question)
    return {
        "answer":response.content,
        "messages": [question, response.content]
    }


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# %%
from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))
# %%
graph.invoke({"question": "대한민국의 수도는 어디인가요?"})


# %%
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

class State(TypedDict):
    messages: Annotated[list[str], add]
    question_length: int

graph_builder = StateGraph(State)

def guardrail(state: State) -> State:
    question_length = len(state["messages"][-1])
    return {
        "question_length": question_length
    }

graph_builder.add_node("guardrail", guardrail)

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: State) -> State:
    question = state["messages"][-1]
    response = llm.invoke(question)
    return {
        "messages": [response.content]
    }

graph_builder.add_node("chatbot", chatbot)

def routing_function(state: State) -> str:
    if state["question_length"] > 3:
        return "chatbot"
    else:
        return END

graph_builder.add_conditional_edges(
    "guardrail",
    routing_function,
    {"chatbot": "chatbot", END: END}
)

graph_builder.add_edge(START, "guardrail")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# %%
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass
# %%
