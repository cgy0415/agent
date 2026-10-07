
from langchain.tools import tool
from pydantic import Field

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

# print(multiply.name)
# # print(multiply.description)
# # print(multiply.args)

@tool
def python_exec_tool(
    imports: str = Field(description="import 문만 (예: 'import math'). 함수/클래스 정의나 다른 코드는 넣지 말 것. 필요 없으면 빈 문자열"),
    code: str = Field(description="import 문을 제외한 전체 코드 블록. 함수 정의도 본문까지 모두 여기에 넣을 것"),
) -> str:
    """
    파이썬 코드를 실행하는 도구입니다. 만약 코드 실행에 실패하면 에러 메시지를 반환합니다.
    실행 결과를 확인하고 싶다면 `print(...)`를 사용하여 출력해야 합니다.

    Args:
        imports: import 문만 넣습니다. 함수/클래스 정의는 code에 넣습니다.
        code: import 문을 제외한 전체 코드 블록

    Returns:
        실행 결과 또는 에러 메시지
    """
    try:
        exec(imports + "\n" + code, {})
    except Exception as e:
        return f"코드 실행에 실패했습니다. ERROR: {repr(e)}"

    result_str = f"성공적으로 코드가 실행되었습니다. :\n```python\n{code}\n```"

    return result_str

@tool
def file_write_tool(
    file_path: str = Field(description="생성/수정할 파일의 경로"),
    content: str = Field(description="파일에 작성할 내용")
) -> str:
    """
    파일을 생성하거나 내용을 작성하는 도구입니다.

    Args:
        file_path: 생성/수정할 파일의 경로
        content: 파일에 작성할 내용

    Returns:
        성공/실패 메시지
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"파일 '{file_path}'에 성공적으로 작성했습니다."
    except Exception as e:
        return f"파일 작성 실패: {repr(e)}"