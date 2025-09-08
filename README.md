# PQC_Analyzer: 비양자내성암호 탐지 시스템

Graph RAG 기술을 활용하여 소스 코드 내의 비양자내성암호(non-PQC) 사용 여부를 분석하는 프로젝트입니다.

## ⚙️ 사전 준비

1.  **Neo4j Desktop 설치 및 실행**: [Neo4j 공식 사이트](https://neo4j.com/download/)에서 Desktop 버전을 설치하고, 'pqc-db'와 같은 이름으로 데이터베이스를 생성한 후 **실행(Start)**하세요.
2.  **Ollama 설치 및 실행**: [Ollama 공식 사이트](https://ollama.com/)에서 macOS용 앱을 설치하고 실행하세요. 메뉴 막대에 아이콘이 나타나면 정상입니다.
3.  **LLM 모델 다운로드**: 터미널을 열고 아래 명령어로 사용할 LLM 모델을 미리 다운로드하세요.
    ```bash
    ollama pull llama3:8b
    ```

## 🚀 실행 순서

1.  **프로젝트 설정 (최초 1회)**
    ```bash
    # 프로젝트 폴더로 이동
    cd /path/to/your/PQC_Analyzer

    # 파이썬 가상환경 생성 및 활성화
    python3 -m venv venv
    source venv/bin/activate


    # 라이브러리 설치
    pip install -r requirements.txt
    ```

2.  **지식 그래프 구축 (최초 1회)**
    ```bash
    # 가상환경이 활성화된 상태에서 실행
    python -m src.graph.graph_builder
    ```

3.  **API 서버 실행**
    ```bash
    uvicorn src.api_server:app --reload
    ```

4.  **API 테스트 (새 터미널에서)**
    ```bash
    # ⬇️ 이 명령어를 복사해서 사용하세요.
curl -X POST "http://127.0.0.1:8000/analyze-code" \
-H "Content-Type: application/json" \
-d '{"file_path": "source_to_analyze/risky_app.c"}'
    ```