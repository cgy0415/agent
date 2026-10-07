import os
import datetime
from typing import Optional
from fastmcp import FastMCP
from markitdown import MarkItDown

#FastMCP 서버 인스턴스 생성
mcp = FastMCP(
    name="Document-Parsing-Automation-Server",
    instructions="다양한 형식(PDF, Word, Excel, PPT)의 문서를 파싱하여 통일된 표준 마크다운 양식으로 반환합니다. "
)

#MarkItDown파서 초기화
md_parser = MarkItDown

def format_to_standard_markdown(
        doc_id: str,
        doc_type: str,
        domain: str,
        file_path: str,
        raw_markdown_content: str
) -> str:
    """
    파싱된 원본 텍스트를 통일된 4단계 표준 마크다운 포맷으로 변환합니다.
    """
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].upper().replace(".", "")
    today = datetime.date.today().strftime("%Y-%m-%d")

    standard_template = f"""#[표준 정제 문서] {file_name}

## 1. 메타데이터 (Document Metadata)
- **문서 ID**: {doc_id}
- **문서 종류**: {doc_type}
- **도메인**: {domain}
- **작성일 및 정제일**: {today}
- **원본 파일 경로**: {file_path}
- **원본 파일 형식**: {file_ext}

---

## 2. 문서 요약 (Executive Summary)
> 본 문서는 `{file_name}` 파일로부터 자동 추출 및 정제된 마크다운 문서입니다. 

---

## 3. 본문 상세 내용 (Main Content)

{raw_markdown_content}

---

## 4. 부록 및 참조 (Appendix)
- **파싱 엔진**: MarkItDown + FastMCP Automation
- **상태**: 파싱 성공 (Parsing Completed)
"""

    return standard_template

@mcp.tool()
def parse_and_normalize_document(
    file_path: str,
    doc_id: Optional[str] = "DOC-AUTO-001",
    doc_type: Optional[str] = "일반 산출물/문서",
    domain: Optional[str] = "설비관리/재고관리"
) -> str:
    """
    지정된 경로의 문서"""