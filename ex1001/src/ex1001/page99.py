from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

def add(left, right):
    return left + right

class State(TypedDict):
    messages: Annotated[list[str], add]

def page99_add_messages():
    msgs1 = [HumanMessage(content="Hello", id="1")]
    msgs2 = [AIMessage(content="Hi there!", id="2")]

    result = add_messages(msgs1, msgs2)
    print(result)
    return result

if __name__ == "__main__":
    page99_add_messages()
