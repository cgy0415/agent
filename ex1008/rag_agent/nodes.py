from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage

from retriever import retriever, retriever_tool
from state import AgentState

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: AgentState):
    """
    검색(Retriever) 도구를 바인딩 한 LLM 모델에 현재 메시지 상태를 입력하여 응답을 생성합니다.
    질문이 주어지면 검색 도구를 도구호출 하거나 일반 답변하며 종료할지 결정할 수 있습니다.
    """
    print("----- [CHATBOT] -----")
    messages = state["messages"]
    llm_with_tools = llm.bind_tools([retriever_tool]) 
    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response],
        "question" : messages[-1].content
    }

def retrieve(state: AgentState):
    """
    현재 질문을 기반으로 관련 문서를 검색합니다"""
    print("-------[RETRIEVER]-------")
    question = state["question"]
    relevant_doc = retriever.invoke(question)
    context = ""
    for doc in relevant_doc:
        context += f"Page {doc.metadata['page']+1}: {doc.page_content}\n"

###노드 코드 미완성