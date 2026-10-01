
#step 1 langgraph : 노드 1개짜리 그래프

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#1) state: 노드들이 함께 읽고 쓰는 공유 메모장
class State(TypedDict):
    file_name: str
    message: str

#2) Node: State를 받아서, 바꾸고 싶은 칸만 dict로 돌려주는 함수=> 일하는 사람
def greet(state: State):
    print(f"[greet 노드] 받은 파일명: {state['file_name']}")
    return {"message": f"'{state['file_name']}' 처리를 시작합니다!"}

#3) 그래프 조립: 시작 -> greet -> 끝
builder  = StateGraph(State)
builder.add_node("greet", greet)
builder.add_edge(START, "greet")
builder.add_edge("greet", END)
app = builder.compile()

#4) 실행
result = app.invoke({"file_name": "드론_이슈목록.xlsx", "message": ""})
print("\n[최종 State]")
print(result)