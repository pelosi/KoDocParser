# KoDocParser

PyMuPDF(fitz) 기반의 한국어 PDF 문서 구조화 추출기입니다. AI/LLM의 RAG(Retrieval-Augmented Generation) 파이프라인에 활용할 수 있도록 PDF 문서에서 텍스트, 메타데이터, 좌표, 이미지 정보를 구조화된 JSON으로 변환합니다.

## 프로젝트 배경

RAG 시스템이나 LLM 학습을 위해서는 PDF 문서의 텍스트를 정확하게 추출하고 구조화하는 전처리 단계가 필수적입니다. 이 프로젝트는 다음 목적을 위해 개발되었습니다:

- **PDF 구조화 추출** - 텍스트, 테이블, 이미지 등을 페이지 단위로 정밀 추출
- **레이아웃 좌표 보존** - 텍스트 블록의 (x, y) 좌표 정보를 유지하여 원본 문서 구조 재현 가능
- **RAG 전처리** - 추출된 데이터를 청킹, 임베딩, 벡터 DB 저장으로 이어지는 파이프라인에 제공
- **로컬 처리** - 외부 API 없이 로컬 환경에서 처리하여 보안성 확보

## 주요 기능

- **문서 메타데이터 추출** - PDF 포맷, 제목, 저자, 언어, 페이지 수, 목차(TOC) 등
- **페이지별 텍스트 추출** - 전체 텍스트 및 텍스트 블록(좌표 포함) 상세 추출
- **이미지 정보 추출** - 페이지 내 이미지 데이터 및 메타정보(해상도, 색상공간 등)
- **하이퍼링크 추출** - 문서 내 링크 정보 수집
- **배치 처리** - 대화형 CLI에서 쉼표 구분으로 여러 파일 일괄 처리
- **성능 로깅** - 각 추출 단계별 소요 시간 측정 및 출력
- **고유 문서 ID** - UUID 기반 문서 식별자 자동 생성

## 프로젝트 구조

```
KoDocParser/
├── src/                        # Python 소스 코드
│   ├── main.py                 # CLI 엔트리포인트 (대화형 인터페이스)
│   ├── pdf_parser.py           # 핵심 PDF 파싱 로직 (PDFParser 클래스)
│   └── libs/
│       ├── logger.py           # 성능 측정 로거
│       ├── date_parser.py      # PDF 날짜 형식 변환
│       ├── json_saver.py       # JSON 출력 저장
│       └── types/
│           └── pdf_types.py    # TypedDict 기반 타입 정의
├── dataset/                    # 입력 PDF 문서 저장소
├── output/                     # 추출 결과 JSON 출력
├── .gitignore
└── README.md
```

## 기술 스택

- **Python 3.x** - 메인 개발 언어 (타입 힌트, TypedDict 활용)
- **PyMuPDF (fitz)** - PDF 텍스트, 메타데이터, 이미지, 좌표 추출 라이브러리
- **uuid** - 문서별 고유 식별자 생성
- **re** - PDF 내부 날짜 형식 파싱

## 사용법

### 실행

```bash
python src/main.py
```

### 대화형 인터페이스

```
PDF 또는 이미지 파일명을 입력하세요. (여러 파일은 쉼표로 구분하세요)
Enter을 입력하면 프로그램이 종료됩니다.
파일명(쉼표 구분): sample_document.pdf
```

- 쉼표로 구분하여 여러 파일을 동시에 처리 가능
- 빈 입력(Enter)으로 프로그램 종료

## 데이터 파이프라인

```
[PDF 파일] → [파일 메타데이터 추출] → [문서 메타데이터 추출] → [페이지별 텍스트/좌표/이미지 추출] → [JSON 저장]
                   ↓                         ↓                              ↓
              파일명, 수정일           포맷, 저자, 목차            텍스트 블록, 좌표, 링크, 이미지
```

1. **파일 메타데이터** - 파일명, 수정 시간 추출
2. **문서 메타데이터** - PDF 포맷, 제목, 저자, 언어, 페이지 수, 목차
3. **페이지 콘텐츠** - 텍스트, 텍스트 블록(좌표), 하이퍼링크, 이미지 및 이미지 메타정보
4. **JSON 직렬화** - UUID 기반 문서 ID와 함께 구조화된 JSON 파일로 저장

## 출력 구조

```
output/
└── {uuid}.json                 # 문서별 추출 결과
```

### JSON 출력 예시

```json
{
  "file_metadata": {
    "file_name": "sample_document.pdf",
    "file_time": "2024-02-15 14:30:22"
  },
  "document_metadata": {
    "format": "PDF 1.5",
    "title": "Sample Document",
    "author": "Author",
    "language": "ko",
    "page_count": 19,
    "last_modified": "2024-02-10 09:15:03 (UTC+09:00)",
    "toc": []
  },
  "parsed_content": {
    "document_id": "cac966e8-9a05-4cfe-9961-a63c64ac68b5",
    "full_text": "[전체 텍스트]",
    "page_texts": [
      {
        "page_number": 1,
        "text": "[페이지 텍스트]",
        "text_blocks": [[x1, y1, x2, y2, "텍스트", block_no, line_no]],
        "images": [],
        "image_info": []
      }
    ]
  }
}
```

## 관련 프로젝트

이 프로젝트는 AI/LLM 데이터 파이프라인의 일부로, 다음 프로젝트들과 함께 활용됩니다:

| 프로젝트 | 역할 | 설명 |
|----------|------|------|
| **KoFinCorpus** | 데이터 수집 | 금융 도메인 PDF/문서 코퍼스 수집기 |
| **KoDocParser** | 로컬 파싱 | PyMuPDF 기반 PDF 구조화 추출 (본 프로젝트) |
| **KoDocAI** | AI 파싱 | Upstage Document Parse API 기반 AI 문서 파싱 |

## 의존성

| 패키지 | 용도 |
|--------|------|
| PyMuPDF (fitz) | PDF 문서 파싱 및 텍스트/이미지 추출 |

## 라이선스

Private
